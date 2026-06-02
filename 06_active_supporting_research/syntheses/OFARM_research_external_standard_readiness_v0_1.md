# External standard readiness for OFARM

> Source note (migration cleanup, 2026-04-10): This report preserves a prior Deep Research synthesis. Inline web/file citation markers were removed during packaging cleanup because their source handles were not portable into the migrated project. Treat the report as supporting research and re-verify external claims before promoting any recommendation into active law.

## Executive summary

1) Must include now: treat cross-domain semantics as a hard, small “semantic substrate” (RDF/OWL + SHACL + the specific geo/time/unit/provenance/observation ontologies), because OFARM already relies on a graph-pattern-first query model, governed validation, and explainable derivation. If these foundations are not explicitly standardised and profiled, interoperability becomes “export-only” and brittle.

2) Must include now: keep the Capability Manifest narrow and contract-like (deployment self-description grounded in active registry state), and align it to mainstream discovery/documentation patterns (OpenAPI for HTTP surfaces; AsyncAPI for event surfaces; `.well-known` for discovery locations). OFARM is explicitly trying to prevent “manifest as ontology blob”, and that’s the right constraint.

3) Must include now: OFARM should formally profile GeoSPARQL (not merely “support geometry”), because GeoSPARQL gives a shared RDF vocabulary and query semantics for geospatial relationships and functions, and GeoSPARQL 1.1 explicitly expects SHACL-based validation patterns and profile framing.

4) Must include now: treat “time semantics” as OWL-Time in the substrate, and be strict about serialisation (ISO 8601 / RFC 3339 timestamps in payloads) while keeping temporal reasoning in the semantic layer. OWL-Time is explicitly designed for temporal properties and topological relations among instants/intervals, which matches OFARM’s need to express evaluation-time policies and event timing without inventing a bespoke time ontology.

5) Must include now: make units and quantities interoperable by anchoring semantics in QUDT but supporting UCUM unit codes in exchange payloads. QUDT provides OWL semantics suitable for reasoning and consistent dimensional modelling; UCUM is explicitly designed for unambiguous machine-to-machine unit expressions and has a defined conformance model.

6) Profile soon: AIM is the best available “agri semantic pivot” for shared agricultural domain semantics right now, but OFARM should not adopt AIM wholesale as OFARM’s operational truth model. AIM’s strongest role is as a layered, modular cross-domain + ag-domain vocabulary with published JSON-LD contexts and SHACL shapes, explicitly intended to harmonise cross-domain standards and multiple ag-domain models. That makes it a high-value alignment anchor and mapping hub, not OFARM’s constitutional meaning.

7) Map only: NGSI-LD (and “Smart Data Models” in the FIWARE ecosystem) are strong runtime integration surfaces for context-broker style systems, but they are structurally and operationally mismatched to OFARM’s assertion/history-first authority, promotion controls, and governed current-state materialisation. Treat NGSI-LD as an exchange/runtime façade (import/export + event subscription), not a semantic core.

8) Map only: ADAPT, ISOXML, and EFDI should be treated as “field operations data interchange surfaces” with explicit loss-maps and provenance rules on ingest. They are important because they exist in real machinery and FMIS pipelines, but they should not become canonical OFARM semantics (or OFARM becomes a thin transliteration engine).

9) Profile soon: EPCIS/CBV is the strongest “traceability events” standard worth serious inclusion, but only as an export/import mapping for MaterialEvent and related custody/transformation semantics, not as OFARM’s internal event grammar. EPCIS’s event framing (what/when/where/why, plus standard query/capture interfaces) is a good interoperability target; OFARM’s internal promotion matrix and authority semantics should remain OFARM-owned.

10) Avoid for now: do not make “credentials = truth” the centre of OFARM. Use W3C Verifiable Credentials as a portable attestation wrapper around OFARM DocumentAssembly outputs where useful, but keep OFARM’s evidence/promotion/governance law as the system of record.

## Standards landscape map

The key judgement OFARM needs to make repeatedly is: semantic anchor vs runtime surface vs exchange format. OFARM’s architecture already separates internal query law (QuerySpecification + QueryPlanIR) from any public textual syntax, and already formalises pack composition and deterministic conflict handling. That architecture strongly favours “profile + mapping surfaces” over “adopt someone else’s runtime model as canonical”.

The following map is deliberately opinionated: recommended action is expressed in the required categories.

| Candidate standard / ontology | Best for | Layer | OFARM stance | Confidence |
|---|---|---|---|---|
| AIM (Agriculture Information Model) | Shared agri vocabulary; bridging multiple ag models; JSON-LD contexts + SHACL validation; cross-domain alignments | Semantic anchor + profile hub | Profile soon (selective import + OFARM profiles); align to it for shared ag semantics; do not make it the OFARM operational truth model | High |
| GeoSPARQL 1.1 | Geospatial RDF vocabulary + geospatial query extensions; SHACL validation patterns; profile framing | Semantic anchor | Must include now (as substrate; OFARM profiles for farm/field/zone/lot geometry expectations) | High |
| OWL-Time | Temporal concepts; relations among instants/intervals; durations; temporal position | Semantic anchor | Must include now (as substrate); profile for OFARM evaluation-time policy + event timing | High |
| PROV-O | Provenance interchange, specialisable; entities/activities/agents | Semantic anchor | Must include now (as substrate); profile for OFARM authority/evidence lineage and materialisation basis | High |
| SOSA/SSN | Observation/actuation/sampling semantics; alignable with O&M and naturally with PROV | Semantic anchor | Must include now (as substrate); profile for OFARM ObservationEvent + evidence linkage | High |
| QUDT | OWL semantics for quantities/units/dimensions, supports reasoning | Semantic anchor | Must include now (semantic); profile for allowed unit/kind sets relevant to farming and lab results | High |
| UCUM | Unit code system for unambiguous electronic communication + conformance tiers | Exchange format / binding | Profile soon (as exchange binding alongside QUDT); do not replace QUDT semantics | Medium |
| SHACL | RDF graph validation language | Profile / conformance artifact | Must include now (validation backbone for semantic profiles, including GeoSPARQL/AIM profiles) | High |
| SPARQL 1.1 | RDF query semantics; graph patterns, optionality, unions, etc. | Query language reference | Align only (semantic reference and inspiration); do not standardise SPARQL as OFARM’s canonical end-user surface in v2 | High |
| OGC API Features + CQL2 | Widely used web geospatial querying; CQL2 text + JSON encodings; optional conformance classes | Runtime surface | Profile soon (as integration façade for geospatial feature access + filtering); map OFARM QuerySpecification filter subset ↔ CQL2 | High |
| ADAPT Standard | Field production data schema for B2B exchange; successor to ADAPT Framework | Exchange format | Map only (import/export packs + loss maps); do not make canonical semantics | High |
| ISOXML (ISO 11783-10 TaskData) | Machinery task controller/FMIS interchange file set | Exchange format | Map only (import/export); do not canonicalise | High |
| EFDI (ISO 5231:2022) | Extensible communication concept/guidelines between machines and FMIS; scenario sets/flows | Runtime/exchange | Map only (integration surface); treat as transport/message profile layer | Medium |
| NGSI-LD API + Information Model | Context information API + property-graph meta-model with RDF basis; JSON-LD serialisation | Runtime surface | Map only (interop façade); do not adopt NGSI-LD entity/property model as OFARM core | High |
| SAREF4Agri | IoT agriculture OWL ontology extension of SAREF | Semantic alignment | Align only (device/irrigation/IoT semantics); do not try to force whole OFARM farm operations into it | Medium |
| EPCIS 2.0 + CBV | Traceability event messaging + controlled vocab for event dimensions | Exchange + semantics for traceability | Profile soon (export/import mapping for traceability events, especially MaterialEvent); do not replace OFARM event grammar | High |
| W3C Verifiable Credentials 2.0 | Portable cryptographically verifiable claim containers | Attestation wrapper | Map only (wrap DocumentAssembly + signatures/attestations); avoid making VC the truth substrate | Medium |
| INSPIRE (agri facilities, cadastral parcels, CRS, etc.) | EU spatial data models + exchange obligations; UML/XSD + mapping tables | Exchange profile (geo compliance) | Map only (geo/regulatory interchange profiles), especially for parcel/boundary datasets; avoid pulling UML/XSD into OFARM core | Medium |
| AGROVOC | Broad multilingual agri thesaurus in RDF/SKOS | Vocabulary bridge | Align only (terminology, concept scheme bindings); do not treat as precise operational ontology | Medium |
| EPPO Codes | Harmonised plant/pest coding system for data exchange | Code system binding | Profile soon (bindings for crops/pests/pathogens; used in pack vocab bindings) | High |
| BBCH scale | Standard phenological growth stage codes (two-digit) | Code system binding | Profile soon (phenology submodule; key for observations/events) | Medium |

Internal OFARM constraint that changes the above recommendations: packs must declare touched surfaces and merge rules, and the default on unsafe overlap is deterministic failure or governance—not “best effort” merging. That makes “standard readiness” naturally implementable as packs/profiles/mapping modules, not as a sprawling monolith.

## Recommended OFARM standard stack

OFARM becomes “externally standard-ready” fastest if it hardens four layers and is ruthless about what is canonical at each.

Shared semantic substrate (must include now)
This layer is the only place where OFARM should “include” external semantics as dependencies. Target: stable, cross-domain primitives and a small number of shared domain anchors.

- RDF/OWL semantics plus SHACL validation as the baseline mechanism to express and validate profiles.
- GeoSPARQL 1.1 for feature/geometry semantics and spatial relationships.
- OWL-Time for instants/intervals and temporal relations.
- PROV-O for provenance (agents/activities/entities), profiled to OFARM’s authority and evidence traces.
- SOSA/SSN for observation/sampling/actuation semantics, aligned to provenance where needed.
- QUDT for quantity/unit semantics; UCUM as a payload binding where external systems expect unitCode strings.

OFARM-owned operational/compliance layer (stay OFARM-owned)
This is where OFARM should not surrender to “famous standards”, because this is the part that makes OFARM not a thin wrapper.

- Truth semantics: event-family grammar, commit classes, and the promotion matrix that prevents weak inputs from silently becoming hard truth. Mapping can exist, but the promotion rules are OFARM-owned.
- Assertion/history-first authority and the authority policy model: external provenance models can be profiled, but OFARM’s governance semantics are the differentiator.
- Current-state materialisation: must retain explainable basis and freshness (FRESH/STALE/INVALID) and must enforce recomputation/refusal for high-consequence actions. External “digital twin APIs” do not provide this; it must remain OFARM law.
- Pack law: deterministic composition, touched-surface declarations, and surface-specific merge semantics. This is how “profiles” can be safely installed without fragmenting meaning.
- Compiled output taxonomy: keep PassportView distinct from frozen DocumentAssembly outputs; this boundary is essential when you later wrap outputs as attestations/credentials.

Runtime/integration layer (profile soon)
This is where OFARM should be pragmatic: adopt common API surface standards, but only as façades over OFARM semantics.

- OGC API Features + CQL2 as an outward-facing geospatial query/filter façade for “feature-like” projections and datasets. CQL2 has explicit text + JSON encodings and conformance-class structure, which aligns with OFARM’s desire for testable surface contracts.
- CloudEvents as an event envelope for inter-service delivery (metadata standardisation), without replacing OFARM’s internal event grammar.
- OpenAPI for HTTP endpoints and AsyncAPI for message/event channels; use these specifically to make Capability Manifest claims verifiable and tooling-friendly.

Mapping/profile surface only (map only, unless a specific profile is warranted)
This is where most “ag standards” belong if OFARM wants interoperability without becoming a transliteration engine.

- ADAPT Standard (and legacy ADAPT Framework ingestion) as import/export mappings. Use explicit coverage + loss maps; treat “ADAPT shape” as an exchange dialect, not meaning.
- ISOXML / ISOBUS TaskData as a high-friction but necessary machinery interchange mapping. ISO’s own description makes clear ISO 11783-10 covers the task controller applications layer and the FMIS interchange format, but it does not make ISOXML semantically rich enough to become OFARM truth.
- EFDI / ISO 5231 as a communications concept/guideline layer for machine↔FMIS↔FMIS data exchange; treat it as a transport/scenario surface with OFARM mappings per scenario flow.
- NGSI-LD as a context-broker integration option: its formal basis is property-graph derived with RDF semantics and JSON-LD serialisation, but its operational model is still an entity/property/relationship context store, not a governed truth/promotion system. Map to/from it; don’t become it.
- SAREF4Agri as a partial semantic alignment target for IoT device/irrigation/measurement contexts, not as the farm operations data model.
- EPCIS/CBV as traceability event export/import: it is explicitly a traceability event messaging standard intended to share event data in a common language; CBV provides the vocabulary dimensioning (what/when/where/why). That’s valuable for supply chain boundaries, but OFARM should keep its own event grammar and evidence promotion rules internally.
- Verifiable Credentials as an optional attestation wrapper for DocumentAssembly outputs (especially SubmissionAssembly), not as OFARM internal truth. VC 2.0 explicitly models credentials as sets of claims with cryptographic verification; OFARM truth is stronger and more nuanced than “signed JSON”.

## Formal inclusion strategy

The technical mistake to avoid is “import everything and hope it lines up”. OFARM’s own architecture already puts you on the right track: formal schemas for query contracts; strict pack merge semantics; and explicit links between runtime claims and active artefact state.

In practice, standard readiness should be packaged as four explicit artefact types.

Inclusion artefacts (must include now)
Purpose: declare the substrate dependencies as normative and versioned (so every deployment and pack knows exactly what semantics are assumed).

- Maintain a versioned substrate bundle importing GeoSPARQL, OWL-Time, PROV-O, SOSA/SSN, QUDT, plus SHACL for validation. GeoSPARQL’s own evolution (GeoSPARQL 1.1 and its profile framing) is a reminder that “geo semantics” is not just WKT-in-JSON.

Profile artefacts (profile soon)
Purpose: constrain and specialise included standards to OFARM’s needs, and make conformance testable.

- Express profiles primarily as SHACL shapes (for RDF graphs) plus JSON Schema (for OFARM JSON artefacts like QuerySpecification and Capability Manifest). This mirrors AIM’s publication approach (OWL modules + JSON-LD contexts + SHACL validation), which is the correct pattern for semantic interoperability that still needs implementability.
- Profile structure should align with OFARM’s pack surface families: vocabulary bindings, template constraints, validation rules, decision rules, event subtypes, view/document shaping, and import/export mappings all have different safe merge semantics. Profiles must declare which surfaces they touch, otherwise “standard alignment” will explode determinism.

Mapping artefacts (map only)
Purpose: define actual translational mechanics to/from external exchange standards; always accompanied by loss maps.

- Each mapping must publish a coverage statement: what external constructs are covered; what are dropped; what are approximated; and what OFARM concepts are required but have no source in the external payload. This is especially non-negotiable for ISOXML, EFDI, and ADAPT, where data is often partial or shaped by device/vendor constraints.
- Mapping must respect OFARM’s promotion matrix: external payloads should normally enter as operation claims / observation assertions / evidence records, not auto-promote into “accepted executed intervention consequence” or “compliance fact” without the governed path.

Conformance-claim artefacts (must include now)
Purpose: make interoperability claims machine-checkable and comparable.

- Capability Manifest should carry minimal conformance claims and link them to test-suite references and declared profile references; crucially it must ground claims in the active artefact set and registry relation, not just marketing text.
- For external standards with explicit conformance classes (e.g., OGC API Features filtering and CQL2, GeoSPARQL’s SHACL validation patterns), OFARM should define “OFARM profile conformance classes” that are: (a) testable; (b) narrow; (c) attachable via manifest claims; and (d) installable as packs/profiles.

## Red flags

1) Don’t make NGSI-LD the canonical internal model. NGSI-LD explicitly formalises a property-graph meta-model with RDF underpinnings and JSON-LD serialisation, but it is still an operational context-store API; it will push OFARM towards CRUD-ish “state is truth” behaviour unless aggressively contained as a façade.

2) Don’t adopt AIM as a monolithic canonical ontology. AIM’s value is that it harmonises and aligns cross-domain standards with multiple ag-domain models and publishes machine-actionable resources (OWL, JSON-LD contexts, SHACL). If OFARM “becomes AIM”, OFARM loses its right to define operational truth/promotion/governance independently.

3) Don’t canonicalise ISOXML/ADAPT/EFDI semantics. They matter as exchange surfaces, but they are not designed to embody OFARM’s authority model, evidence sufficiency, or deterministic pack composition. Canonicalising them would make OFARM a compatibility wrapper rather than a semantically native operating standard.

4) Don’t let public query syntaxes drive internal law. OFARM already states “internal model first, public syntax later” via formal QuerySpecification and QueryPlanIR schemas. Copying SPARQL/CQL2 wholesale as OFARM’s constitutional query contract would force premature surface freezing and conflate internal semantics with external convenience syntax.

5) Don’t treat EPCIS as a general farm event model. EPCIS is a traceability event messaging standard; it is excellent at supply chain visibility events, but weak at OFARM’s on-farm governance, evidence sufficiency, and promotion semantics. Use it for boundary exchange, not internal authority.

6) Don’t let credentials replace authority. Verifiable Credentials are claim containers with cryptographic verifiability; they do not encode OFARM’s “why this became in-force truth” logic. If VC becomes canonical, you either (a) lose OFARM’s explainability; or (b) cram OFARM governance into credentials and recreate OFARM inside VC—worse.

## Prioritized next actions

1) Publish an explicit “OFARM Semantic Substrate” artefact that version-pins GeoSPARQL, OWL-Time, PROV-O, SOSA/SSN, QUDT, and SHACL; define OFARM-required conformance checks (SHACL shapes) for each.

2) Create an “AIM Alignment Profile Pack” that: (a) imports the AIM modules OFARM actually needs; (b) defines SHACL constraints for OFARM’s required interpretation; and (c) publishes OWL/SKOS mapping assertions between OFARM core concepts and AIM where stable. Treat this as a profile pack with declared touched surfaces and merge semantics.

3) Define an “OFARM ↔ NGSI-LD Bridge RFC” that restricts scope to a small set of projections (e.g., farm/field/parcel, selected observations, selected interventions, selected lots) and explicitly states what is lost in each direction; include a rule that NGSI-LD ingest does not auto-promote beyond operation claim / observation assertion / evidence record.

4) Define an “OFARM ↔ EPCIS 2.0 Traceability Pack” that maps MaterialEvent and custody/transformation/split/merge semantics into EPCIS event structures with CBV vocab usage; publish a coverage statement and loss map; require provenance links back to OFARM authority.

5) Define an “OFARM ↔ ADAPT Standard Pack” with JSON Schema validation on ingest, explicit field-operation coverage matrix, and strict unit handling (QUDT semantics + UCUM codes in payloads where present).

6) Define an “OFARM ↔ ISOXML/EFDI Machinery Interop Pack” that treats ISOXML and ISO 5231 flows as input evidence/claims, defines canonical normalisation rules, and publishes scenario-by-scenario coverage statements (especially where ISO 5231 scenario flows are used).

7) Extend QuerySpecification filter semantics with an explicit mapping subset to CQL2 (where possible) and to NGSI-LD query patterns (where possible), but keep QuerySpecification as the constitutional contract and keep any textual syntax out of v2.

8) Standardise service discovery: define `.well-known/ofarm-capabilities` (or equivalent) that returns the Capability Manifest, and require OpenAPI/AsyncAPI documents (or references) inside the manifest for the declared surfaces. This makes capability claims testable via tooling instead of tribal knowledge.

9) Define a “DocumentAssembly Attestation Profile” that maps OFARM DocumentAssembly outputs into Verifiable Credentials only at the boundary where third parties need portable cryptographic attestations; explicitly state that VC validity does not imply OFARM truth without the referenced authority basis.

10) Add a conformance-claim taxonomy to the Alignment Register that separates: (a) semantic anchor conformance (substrate); (b) profile conformance (packs/profiles); (c) mapping conformance (import/export packs); (d) runtime surface conformance (API façades). The Capability Manifest already has the structure to carry minimal conformance claims; finish the taxonomy so claims are comparable across deployments.
