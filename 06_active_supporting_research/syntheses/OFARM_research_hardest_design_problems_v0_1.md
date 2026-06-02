# Deep research on best practices, papers, and analogues for OFARM’s hardest design problems

> Source note (migration cleanup, 2026-04-10): This report preserves a prior Deep Research synthesis. Inline web/file citation markers were removed during packaging cleanup because their source handles were not portable into the migrated project. Treat the report as supporting research and re-verify external claims before promoting any recommendation into active law.

## Executive summary

OFARM’s baseline already encodes several “correct but non-obvious” architectural stances—assertion/history-first authority, governed current-state materialisation with explicit freshness, strict commit classes, pack/profile merge law, and explicit action-based authority—whose closest real-world analogues tend to be **medico-legal EHR architectures**, **supply-chain traceability event standards**, and **large-scale cloud authorisation systems** rather than generic ontology work.

The deepest risk is not whether OFARM can model agriculture, but whether OFARM can keep its **operational semantics deterministic, auditable, and explainable** while supporting (a) offline field capture, (b) multi-party workflows, (c) modular regulatory/certification context, and (d) AI assistance without silent truth mutation. This is exactly the failure mode that standards like EPCIS try to prevent via explicit event semantics + validation artefacts, and that openEHR tries to prevent via append-only versioning + contributions + attestations.

A decisive pattern: treat “current state” as a **derived, governed projection** whose provenance is itself first-class. This is the shared spine across event sourcing (state rebuildable from an event log), CQRS (separate write and read models), temporal databases (system time vs application time), openEHR version repositories (rollback via contributions/versions), and EPCIS (eventTime vs recordTime with capture semantics).

Identity is where crop-farming “looks easy” but becomes hard: the moment you support split/merge/commingling/transformation, you need a **cohort/lot algebra** (what persists, what branches, what merges, what invalidates claims) that is closer to chain-of-custody standards (ISO 22095 models; EPCIS transformation/aggregation semantics) than to typical farm CRUD systems.

For modular context (packs/profiles), the non-negotiable is: **profiles are constraints; packs are governed artefact bundles; composition must be deterministic**. The strongest analogues are (a) FHIR profiling (differential vs snapshot; canonical artefact versioning), (b) openEHR archetype/template governance and identification (stable IDs, aliasing, lineage), and (c) mature module systems that enforce dependencies and versioning at runtime (OSGi).

Authority/delegation/sharing/revocation is an architectural subsystem, not a feature. The best “stress-tested” reference is the Zanzibar paper (relationship-based access control at global scale) combined with formal ABAC foundations (NIST SP 800-162) and policy-composition mechanics (XACML combining algorithms as a concrete precedent for deterministic merge law). Capability-style delegated credentials (Macaroons; modern capability tokens like Biscuit) are relevant specifically for **offline attenuation and delegation**, but must be paired with revocation strategy (OAuth token revocation) and auditability.

Internal query architecture benefits from copying one core lesson from SPARQL and AQL: stable semantics come from **graph-pattern-first querying**, plus a disciplined path system that is versioned and resolvable against governed structures. OFARM’s SemanticPathAlias is best treated like a *governed compatibility contract* akin to FHIRPath’s role in FHIR and openEHR path usage in AQL—powerful, but dangerous if allowed to drift.

Evidence and attestation should be modelled as a **claims–evidence–provenance system**, not merely “attachments”. Strong analogues: structured assurance cases (SACM: explicit claims/arguments/evidence), digital evidence chain-of-custody guidance (NIST IR 8387; ISO/IEC 27037), and verifiable credentials/signature envelopes for portable attestations (VC Data Model 2.0 + JWS). The key OFARM consequence: evidence sufficiency becomes a first-class, testable policy layer, not ad hoc “required fields”.

Field/mobile UX must implement “capture is not commit” as a **visible workflow invariant**. The most reliable field tooling ecosystems (e.g., ODK, KoboToolbox) treat offline capture as device-stored drafts and explicitly upload/finalise later—this maps cleanly to OFARM commit classes and gates, but only if OFARM adds strong stale-state cues and conflict/ambiguity workflows. For local-first concurrency, CRDTs are useful for *draft-layer convergence*, but should not be used to auto-merge compliance truth.

For trustworthy human–AI interaction, OFARM should operationalise two evidence-backed guardrails: (1) AI suggestions must be clearly separated from committed truth and placed into a governed pipeline; (2) interfaces should aim at calibrated trust, not maximal automation. The most-cited baseline is Amershi et al.’s Human–AI interaction guidelines, complemented by the NIST AI RMF framing of trustworthiness as risk-managed socio-technical practice.

A non-obvious but high-leverage transfer: OFARM’s capability manifest should copy the *function* (not the domain) of FHIR CapabilityStatement and OpenAPI/WoT Thing Descriptions—machine-readable, deployment-specific truth about what is actually supported—because ecosystem conformance at scale depends on self-description that can be validated.

Conformance at scale is not “later”. The best standards ecosystems publish **normative validation artefacts** (JSON Schema, SHACL shapes, OpenAPI) alongside prose. EPCIS does this explicitly; SHACL formalises constraint validation for RDF graphs. OFARM’s “bounded debt” items (template-merge validators, alias stability, trace-object schemas) should be treated as conformance artefact backlogs, not implementation niceties.

## Problem-by-problem analysis

**Identity and lifecycle semantics**

Why it is hard: farming has *multiple overlapping identity axes*—physical geography (field boundary revisions), management intent (zones that are durable vs ephemeral overlays), biological/cycle identity (crop cycle continuity vs replant), and material cohort identity (lots under custody, split/merge, commingling, transformation). OFARM’s own baseline correctly distinguishes durable identity vs identity revision vs time-bounded state, and requires explicit lineage relations for split/merge/replacement/overlap.

Best external approaches found:
- **Supply-chain traceability event standards**: EPCIS makes the split/merge problem explicit via event types like AggregationEvent (add/remove/observe parent–child relations) and TransformationEvent (inputs consumed; outputs produced; with explicit semantics for input/output lists and optional grouping by transformationID). This is directly reusable as a conceptual analogue for lot lineage under repacking, blending, processing, and disposal.
- **Chain-of-custody model taxonomy**: ISO 22095 treats chain-of-custody systems as selecting among models with different physical mixing semantics and levels of “presence of claimed characteristics” (identity preserved, segregated, controlled blending, mass balance, book-and-claim). This maps neatly to OFARM lot semantics because “lot identity” is not only physics; it is also *which claims remain justified under mixing*.
- **Provenance graph foundations**: PROV-O provides a widely used backbone for representing entities, activities, agents, and derivation/attribution; it is often the best cross-domain anchor for lineage semantics even when OFARM owns domain-specific lifecycle relations.
- **Industrial lifecycle integration** (useful mainly as a warning): lifecycle standards like ISO 15926 target cross-disciplinary lifecycle data integration with a single meaning context; they demonstrate both the value and complexity of “one referent through lifecycle views”—and thus reinforce why OFARM must keep identity rules tight and testable.

Where these fit OFARM well:
- EPCIS provides concrete, field-tested semantics for “this cohort became part of that cohort” (aggregation) and “these inputs produced these outputs” (transformation), including the important nuance that observation may be incomplete and that parent IDs may be unknown in OBSERVE actions. That is exactly the kind of real-world messiness OFARM wants to preserve without faking certainty.
- ISO 22095 provides a vocabulary for different commingling regimes; OFARM can use it to prevent category errors like treating mass-balance attestations as identity-preserved traceability.

Where they do not fit:
- EPCIS is optimised for cross-enterprise event exchange; it does not give you an “operational semantics kernel” for agronomy (planned vs executed interventions, compliance commit classes, advisory separation). OFARM must not collapse into “EPCIS for farms”.
- ISO 22095 is intentionally generic and largely management-system adjacent; OFARM should borrow its model taxonomy, not its process language.

Recommended direction for OFARM:
- Define a **Lot/TraceObject algebra** explicitly (bounded-debt: *lot edge-case maturity*; *trace-object schema formalisation*). Make “split”, “merge/commingle”, “transform”, and “reclassify claim basis” first-class lifecycle operations with mandatory lineage edges and evidence hooks, using EPCIS-style transformation semantics as the conceptual starting point (inputs may contribute to all outputs; transformationID groups multi-step transformations).
- Add an explicit **chain-of-custody model attribute** (or equivalent) to lots/claims where commingling occurs, aligned to ISO 22095’s model taxonomy, so that query and document assembly can qualify what kind of claim remains valid after mixing.

What not to copy:
- Do not copy a “single lot ID that survives anything” model. EPCIS and chain-of-custody practice show that split/merge/transformation inevitably creates new traceability objects/events; pretending otherwise deletes the reasoning basis for claims.

**Assertion/history-first truth with governed current-state materialisation**

Why it is hard: the difficult part is not append-only storage—it is (a) multi-temporal semantics, (b) contradiction and supersession without deletion, and (c) high-consequence recomputation with explainable basis. Temporal DB research and practice emphasise that “time” is not one axis; bitemporal models distinguish valid time vs transaction time, and SQL:2011 formalises both system-versioned and application-time periods (and can combine them for bitemporal tables).

Best external approaches found:
- **Event sourcing + CQRS**: event sourcing treats state as rebuildable from an event log; CQRS formalises different models for writes vs reads (helpful when “current state” is a governed projection). Fowler’s warning is relevant: CQRS adds risky complexity unless the problem truly demands it—which OFARM does, because the compliance/advisory split, evidence, review, and freshness policies are inherently complex.
- **openEHR version repositories**: openEHR’s Common Information Model shows a mature medico-legal approach where commits are grouped into Contributions (change-sets), versions reference contributions and audits, and rollbacks are possible by replaying/inspecting the contribution history. It also treats attestation as a post-commit operation that creates additional audit/attestation objects rather than rewriting history.
- **EPCIS eventTime vs recordTime**: EPCIS explicitly treats recordTime as the time of capture by the repository/accessing application, and distinguishes it from eventTime; recordTime can be omitted on input and is then set at capture. This mirrors OFARM’s need to preserve late-arriving assertions/evidence without falsifying “when we learned it”.

Where these fit OFARM well:
- OFARM’s “assertion/history-first authority + governed current-state materialisations with a MaterialisationBasis + freshness state” is essentially CQRS with stronger governance and explainability requirements.
- openEHR strengthens the case for treating “commit” and “attest/sign” as separate governance events and for keeping auditable change-sets.

Where they do not fit:
- Pure event sourcing typically treats domain events as the authoritative log of state change. OFARM’s architecture is stricter: events exist, but *accepted event consequences* and reviewed assertions determine what becomes in-force current state. That is closer to audited clinical recordkeeping than to typical event-sourced ecommerce systems.

Recommended direction for OFARM:
- Treat OFARM’s temporal model as a **deliberate tritemporal+governance model** (bounded-debt: *current-state freshness-policy deepening*). Use temporal DB vocabulary to keep axes crisp: event/observation time (real-world), assertion/record time (system capture), and decision/supersession time (governance). Temporal DB literature explicitly distinguishes these notions (valid vs transaction time; decision time appears as an additional axis in temporal modelling discussions).
- Make MaterialisationBasis explainability non-optional for high-consequence actions, mirroring EPCIS’s emphasis on capture semantics and openEHR’s auditable contribution trail.

What not to copy:
- Do not allow “read model fixes” that bypass the authoritative log/graph. CQRS literature is clear that split read/write models become dangerous when teams “patch” the read side to compensate for missing truth discipline.

**Pack/profile/context modularity**

Why it is hard: modular context is a semantic versioning and conflict-resolution problem disguised as “config”. Without strict composition law, packs become plugins; plugins become chaos; chaos destroys standard-grade determinism. OFARM already fixes precedence classes, surface families, and merge modes with hard-fail defaults.

Best external approaches found:
- **FHIR profiling mechanics**: FHIR distinguishes an authoring-friendly *differential* (constraints relative to a base) from an operational *snapshot*; operational tooling can generate snapshots from differentials. This is an exact conceptual analogue to OFARM’s “deep truth vs governed materialisation” mindset—but for schema constraints.
- **Canonical artefact lifecycle and registries**: the FHIR CRMI IG focuses on consistent lifecycle management of computable artefacts from authoring through publishing and implementation, including the existence of artefact repository services and lifecycle concerns. That maps to OFARM’s pack/profile governance and registry needs.
- **openEHR archetype governance and identification**: openEHR’s identification spec explicitly tackles stable identification, versioning, transfer/forking, aliasing, and integrity/non-repudiation for knowledge artefacts, including the idea that a GUID remains stable across changes and that identifier aliasing is an explicit mechanism. This is highly relevant to OFARM packs/templates/rules as installable artefacts.
- **Runtime module systems**: OSGi demonstrates a strict model where bundles carry explicit manifests that declare dependencies required for activation; the framework resolves dependencies using those versioned declarations. This is conceptually close to OFARM pack manifests + activation-set compatibility checks.

Where these fit OFARM well:
- FHIR + openEHR together provide a strong blueprint for “profile as constraints” and “artefact lifecycle as governed product”, including canonical identifiers and versioning practices.
- OSGi offers a reference for deterministic activation driven by explicit metadata rather than runtime guesses.

Where they do not fit:
- FHIR’s ecosystem accepts substantial variability in profiling quality and relies heavily on community conventions and tooling; OFARM will need stricter merge law because OFARM packs can change evidence policy and compliance consequences, not just message shape.

Recommended direction for OFARM:
- Elevate “pack merge” to a **formally validated compilation step** (bounded-debt: *template-merge validator maturity*). Treat each PackActivationSet as producing a deterministic “effective context snapshot” the way a snapshot profile represents effective constraints.
- Publish normative validation artefacts for merged context (SHACL/JSON Schema style). EPCIS ships JSON Schema and SHACL validation files as normative artefacts; SHACL itself is a W3C Recommendation for validating RDF graphs. This is exactly the move OFARM needs for pack/template merge determinism.

What not to copy:
- Don’t copy “stringly-typed extension points” or ungoverned overrides. Both FHIR and openEHR emphasise formal artefact identity and conformance testing; EPCIS forbids silent drift by publishing normative schemas/shapes.

**Authority / delegation / sharing / revocation**

Why it is hard: OFARM needs **action-based, scoped, delegated, revocable, traceable** authority with multi-party workflows and AI assistance under human accountability. This is harder than classic RBAC because farming operations involve contractors, advisors, certifiers, buyers, seasonal staff, and cross-scope actions; plus offline work where authorisations may be stale.

Best external approaches found:
- **Relationship-based access control at scale (Zanzibar)**: Zanzibar is a global system for storing and evaluating permissions across billions of objects; its core contribution is a uniform data model and configuration language for expressing many policy shapes across services—exactly the “one substrate, many contexts” problem OFARM faces.
- **ABAC conceptual foundations (NIST SP 800-162)**: ABAC frames authorisation as evaluating attributes of subject, object, operation, and environment against policy—matching OFARM’s AuthorityActionClass + scope/time/purpose conditions.
- **Policy engines and composition (XACML; OPA/Rego)**: XACML is a mature policy language with explicit combining algorithms (deny-overrides, permit-overrides, ordered variants), which is a direct analogue to OFARM’s need for deterministic merge semantics across packs/policies. OPA/Rego exemplifies “policy as code” operating over structured inputs, which matches OFARM’s enforcement-chain mindset.
- **Delegation credentials (Macaroons; capability tokens)**: Macaroons support decentralised delegation via caveats and attenuation—useful for OFARM delegation grants (especially in offline work) if paired with audit and revocation design.
- **Revocation protocol primitives (OAuth token revocation)**: RFC 7009 defines a token revocation endpoint that invalidates tokens and related tokens derived from the same authorisation grant—useful as a concrete revocation pattern when OFARM grants are expressed as tokens/credentials.

Where these fit OFARM well:
- Zanzibar + ABAC strongly support OFARM’s “default deny unless justified by explicit action path” and its need to produce an AuthorizationDecisionTrace for every consequential action.
- XACML combining algorithms are a concrete reference point for why policy composition must be explicit and deterministic (and why “ordered composition” is a first-class merge mode).

Where they do not fit:
- Zanzibar’s “configuration language + relationship tuples” doesn’t directly cover evidence sufficiency, pack activation, or AI-assisted governance; it is an authorisation kernel, not an operational standard.
- Capability tokens (Macaroons-like) can be hard to revoke without online checks or short-lived tokens + refresh. OFARM must avoid designing delegation that only works when nobody needs to revoke.

Recommended direction for OFARM:
- Implement authority as a **relationship-and-attribute hybrid**: Zanzibar-style relationship tuples for “who can act on what”, plus ABAC-style conditions for time, purpose, pack context, and twin. This fits OFARM’s action-based classes and scoped inheritance modes.
- Treat policy/authority composition like pack merge: define and test combining semantics explicitly (XACML is a practical precedent), and require decision traces.
- For offline delegation, prefer **attenuation-first credentials** (Macaroons-style caveats) only for narrow, time-bounded, auditable actions, and ensure revocation is handled via short expiry + server revalidation at sync/commit.

What not to copy:
- Don’t copy UI-driven authorisation (“if it’s in the workflow, it must be allowed”). Zanzibar exists largely because ad hoc per-application auth breaks at scale; OFARM will face the same compression of edge cases.

**Internal query architecture**

Why it is hard: OFARM needs internal-first querying that preserves semantic meaning across execution targets, supports alias shorthands, and remains stable under evolving packs/templates. This is the same kind of complexity that led openEHR to AQL (query over archetype-based repositories) and that drove SPARQL to standardise graph pattern semantics.

Best external approaches found:
- **Graph-pattern query semantics (SPARQL)**: SPARQL 1.1 formalises graph patterns and adds property paths as a succinct way to describe multi-hop traversals, while preserving the semantics of basic graph patterns.
- **Archetype-aware querying (openEHR AQL)**: AQL is explicitly designed to query archetype-based repositories, and uses openEHR path syntax for both coarse and fine-grained nodes—highly relevant to OFARM’s path alias concept.
- **Property graph query standardisation (ISO GQL)**: ISO/IEC 39075 standardises a database language for property graphs, signalling that the “graph query” space is formalising beyond RDF/SPARQL; OFARM can borrow planning/equivalence ideas even if it does not expose GQL.
- **Query planning IR as a first-class artefact (Calcite)**: Calcite’s research paper is a strong reference for representing queries in relational algebra, applying rule-based transformations while preserving semantics, and pushing down to heterogeneous sources—an architectural analogue for OFARM QueryPlanIR targeting graph engines, projections, and geospatial filters.
- **Path expressions as a standard compatibility surface (FHIRPath)**: FHIRPath is a path-based navigation and extraction language “like XPath”, used pervasively for invariants and querying in FHIR. It is an existence proof that path shorthands become de facto contracts and require tooling/validation to avoid runtime-only failures.

Where these fit OFARM well:
- OFARM’s “QuerySpecification → QueryPlanIR → governed execution” is strongly aligned with established database practice (separate logical semantics from physical plan) and with Calcite’s IR approach.
- AQL and FHIRPath show that if you have archetype/template-bound content, you inevitably need a disciplined path system; OFARM’s SemanticPathAlias should be treated as a governed path contract, not a convenience string.

Where they do not fit:
- SPARQL assumes RDF semantics end-to-end; OFARM’s semantics include governance, twin policies, pack activation, and evidence requirements that aren’t naturally “just RDF triples”. OFARM should borrow graph-pattern principles without inheriting SPARQL’s entire semantic stack.

Recommended direction for OFARM:
- Treat SemanticPathAlias as a **versioned, testable compatibility contract** (bounded-debt: *alias-stability governance*). openEHR identification explicitly discusses identifier aliasing; FHIR canonicals explicitly support version-qualified canonical references; both can be translated into OFARM rules for alias version pinning and controlled evolution.
- Require semantic equivalence tests across execution targets (bounded-debt: *deeper conformance at scale*). Calcite demonstrates rule-based plan rewriting while preserving semantics; OFARM needs the analogous invariant: different QueryPlanIR backends must be provably equivalent at the semantic level.

What not to copy:
- Don’t copy a public, free-form expert query language too early. Both OFARM’s own constitution and openEHR’s experience suggest that you want internal canonical models + tooling first; exposing raw power early increases support burden and accidental semantic drift.

**Evidence, compiled outputs, and attestation**

Why it is hard: you need to answer “why should anyone believe this?” in a way that survives time, dispute, and context change. That requires (a) raw evidence retention, (b) normalised interpretations linked back to raw sources, (c) explicit claims whose basis is traceable, and (d) portable outputs that can be frozen/attested without becoming canonical truth. OFARM’s DocumentAssembly and PassportView split, plus “raw evidence + interpretation” rule, already aligns with this.

Best external approaches found:
- **Structured assurance cases (SACM)**: SACM defines a metamodel for structured assurance cases: auditable claims supported by arguments and evidence. This is one of the cleanest formal analogues for OFARM “evidence sufficiency policies” and for building dossiers/submissions that can be inspected.
- **Digital evidence chain-of-custody guidance**: NIST IR 8387 is directly about digital evidence preservation and chain of custody; ISO/IEC 27037 provides guidelines for identification/collection/acquisition/preservation of digital evidence. These anchor real-world expectations for evidentiary handling and records that may be used in disputes.
- **Portable verifiable attestations**: VC Data Model 2.0 provides a standard model for machine-verifiable credentials; JWS provides JSON-based signature/MAC envelopes. Together they illustrate how OFARM DocumentAssemblies could later be exported as signed/verifiable objects without treating them as “truth”.
- **Conformity assessment vocabulary**: ISO/IEC 17000 provides general terms/definitions for conformity assessment; this can help OFARM stay precise about what is being asserted/attested versus merely claimed.

Where these fit OFARM well:
- SACM provides a rigorous conceptual blueprint for the exact thing OFARM wants: evidence-backed claims with traceable structure—especially relevant to DossierAssembly/SubmissionAssembly semantics.
- NIST/ISO digital evidence guidance gives OFARM a cross-domain baseline for evidence handling quality and chain-of-custody records—even if OFARM’s evidence includes photos, machine logs, lab results, and signed documents rather than “computer forensics”.

Where they do not fit:
- VC-style credential ecosystems introduce privacy, key management, and verifier trust-list complexity; OFARM should treat them as an optional export/attestation format, not as the internal truth substrate.

Recommended direction for OFARM:
- Implement evidence sufficiency as a **policy that compiles into an assurance-case-like structure** (bounded-debt: *trace-object schema formalisation*; *deeper conformance at scale*). Concretely: each high-stakes compliance claim should be representable as (Claim) ← (Argument/Rule) ← (EvidenceBundle + provenance), aligned conceptually to SACM.
- For DocumentAssembly, retain a durable “basis snapshot” similar to openEHR’s medico-legal “what content was attested at that time” stance and to OFARM’s own MaterialisationSnapshot idea.

What not to copy:
- Don’t copy “PDF-centric compliance” where the PDF is treated as truth. Evidence systems repeatedly fail when the compiled artefact becomes the canonical source. OFARM’s separation rule is correct and should remain strict.

**Field and mobile UX for trustworthy capture**

Why it is hard: offline work, ambiguity in field conditions, stale state, and AI assistance create constant pressure to “just accept something” and silently patch later. That pressure must be countered by UX that makes capture/typing/evidence/review status explicit, and by sync logic that re-evaluates authority and context at commit time.

Best external approaches found:
- **Offline-first field capture systems**: ODK is explicitly designed for collecting data “anywhere” and maintaining functionality under limited/no connectivity; KoboToolbox documents that offline collection stores submissions on device first and can upload finalised forms later. These are practical precedents for OFARM’s edge capture posture.
- **Conflict-free replicated data types (CRDTs)**: CRDT theory provides mathematically grounded convergence for replicated data under concurrent updates. This is relevant for OFARM *draft graphs* and collaborative editing, but (critically) should be scoped away from compliance truth materialisation.
- **Human–AI interaction guidance**: Amershi et al.’s guidelines emphasise managing expectations, showing confidence/uncertainty appropriately, enabling efficient correction, and supporting user control—all directly relevant to “AI-assisted data entry without silent truth mutation”.

Where these fit OFARM well:
- ODK/Kobo’s explicit “store locally then upload/finalise” workflow maps directly to OFARM’s “capture is not commitment” and multi-gate enforcement chain.
- CRDTs give OFARM a principled approach for local-first draft convergence *without* granting those drafts authority.
- Amershi’s human–AI guidelines support OFARM’s AI boundary rules by translating them into interaction contracts users can understand (“what did the AI do; what did it not do; how do I correct it”).

Where they do not fit:
- Many offline-first patterns assume eventual consistency plus automatic conflict resolution; OFARM cannot allow “eventual compliance truth” without explicit governance. Therefore, only the draft layer may converge automatically; promotion must remain explicit.

Recommended direction for OFARM:
- Implement a **two-layer offline UI**: (1) local draft workspace that can auto-merge and tolerate inconsistency; (2) explicit “commit to OFARM authority” workflow that triggers re-validation of authority, packs, evidence, and freshness at sync time (bounded-debt: *current-state freshness-policy deepening*).
- Make stale state and basis visible: EPCIS distinguishes eventTime vs recordTime; OFARM should surface analogous distinctions and freshness states in-field (“this view is stale for compliance signing”).

What not to copy:
- Don’t copy “single-step forms that directly update truth.” Field tools that feel fast often do so by collapsing capture and commit; OFARM’s design goal is the opposite.

**Cross-industry analogues that change OFARM design choices**

Key analogues and what they imply for OFARM:

- **Medico-legal record architectures (openEHR)**: openEHR treats audit, versioning, contributions (change-sets), and attestations as core—not add-ons. The direct transfer is the mindset that the *record is evidence* and must support rollback, non-repudiation, and post-commit attestation without rewriting history.
- **Supply-chain traceability standards (EPCIS + ISO chain-of-custody)**: explicit event semantics for aggregation/transformation plus explicit time axes (eventTime/recordTime) are highly transferable to lot lineage and auditability. ISO 22095’s model taxonomy is transferable to how OFARM represents claims under commingling.
- **Industrial digital twins (AAS; ISO 23247)**: AAS formalises a digital representation of an asset with a metamodel and packaging format; ISO 23247 frames a digital twin framework for manufacturing. The transfer is that “digital twin” architectures that survive industry scrutiny are metamodelled, versioned, and packaged—not just ad hoc APIs.
- **Geospatial observation standards (ISO/OGC OMS; SensorThings; GeoSPARQL)**: observation semantics and geospatial querying get formalised so that heterogeneous sources can be integrated. OFARM should keep using these as substrate anchors, particularly for observation evidence.
- **Authorisation systems (Zanzibar; ABAC; XACML/OPA)**: the transfer is that OFARM should treat authorisation as a data model + evaluation engine + decision trace, with explicit composition semantics, not an application-layer convention.

## Cross-industry pattern transfer

What OFARM should borrow (mostly “as-is”, adapted only to farming vocabulary)
- **Event semantics for material cohorts**: EPCIS-style aggregation/transformation semantics (including “observation may be incomplete” and explicit input/output semantics) are a rare example of a standard that directly addresses the hard parts of lot lineage.
- **Explicit capture-time vs event-time**: EPCIS recordTime handling at capture is a practical, normalised precedent for “when the system learned it” vs “when it happened”.
- **Audit + post-commit attestation model**: openEHR’s contribution/version/audit and attestation handling is a strong analogue for separating commit from signing and preserving medico-legal trace.
- **Formal constraint validation artefacts**: SHACL as RDF validation, and EPCIS’s practice of shipping JSON Schema + SHACL + OpenAPI as normative artefacts, are directly transferable to OFARM pack/template/query validation.

What OFARM should adapt (pattern is right; semantics need OFARM-specific law)
- **Profiling/snapshot approach to “effective constraints”**: FHIR’s differential vs snapshot pattern should inspire OFARM’s “effective merged context” compilation, but OFARM must enforce stronger determinism because constraints can affect compliance outcomes.
- **Relationship-based authorisation at scale**: Zanzibar’s relationship tuples align well with OFARM’s action-on-scope model, but OFARM must add twin-aware, evidence-aware, pack-aware conditions and keep decision traces mandatory.
- **Capability self-description as an ecosystem primitive**: treat OFARM Capability Manifest like a domain-specific cousin of FHIR CapabilityStatement and OpenAPI/WoT Thing Descriptions—machine-readable truth about what is actually supported, tied to a registry state.
- **Assurance-case structure for compliance evidence**: SACM’s claims/arguments/evidence structure should inform OFARM evidence sufficiency policies and dossier assembly, but OFARM must encode farming-specific evidence types and governance paths.

What OFARM should reject (tempting, but structurally misaligned)
- **“Book-and-claim everywhere” semantics as a default**: ISO 22095 includes book-and-claim as a chain-of-custody model; OFARM should support it only when the regulatory/certification context explicitly allows non-physical traceability, and should never let it masquerade as identity-preserved lot lineage.
- **Auto-promotion from AI outputs into compliance truth**: this breaks both trustworthy UX and auditability; it conflicts with OFARM’s baseline and the evidence-based HCI guidance that emphasises user control and correctability.
- **Unconstrained plugin ecosystems**: OSGi-like systems exist precisely to avoid dependency/activation chaos; OFARM should not allow “packs that override anything” without declared surfaces and merge law.

## Architectural risk register

| Risk | Severity | Why it matters | Source-grounded mitigation ideas |
|---|---:|---|---|
| Lot identity collapses under split/merge/commingling/transformation, producing unverifiable lineage | Critical | Without a coherent cohort/trace-object algebra, compliance claims and buyer passports become disputable; “lineage” becomes storytelling rather than computable audit | Adopt EPCIS-style aggregation/transformation semantics for lot lineage; explicitly model chain-of-custody regimes (ISO 22095 taxonomy); require lineage edges + evidence hooks for every cohort-changing event |
| Current-state materialisation is not explainable or recomputable on demand (basis drift) | Critical | High-consequence actions depend on current state; if you cannot explain the basis, you cannot defend decisions or attestations | Make MaterialisationBasis mandatory for high-consequence uses; preserve snapshots when relied upon; follow temporal discipline (valid/system time concepts; EPCIS recordTime capture semantics; openEHR auditable contributions) |
| Pack/profile composition becomes non-deterministic (“plugin chaos”) | Critical | If two deployments get different “effective context” from same declared packs, OFARM cannot be standard-grade | Compile PackActivationSet → effective context snapshot; publish normative merge validation artefacts (SHACL/JSON Schema patterns); hard-fail on ambiguous merge; adopt versioned artefact IDs/registry discipline (CRMI/openEHR identification) |
| Alias drift breaks query stability and compiled outputs (“same alias, different meaning”) | High | Stable audit requires the ability to re-run queries and explain outputs later; alias drift undermines reproducibility | Treat aliases like canonical resources: version pinning and controlled evolution (FHIR canonical versioning; openEHR identifier aliasing); conformance tests for alias resolution; fail fast on ambiguous alias resolution |
| Authorisation model fails under delegation/revocation/offline, causing either over-permission or unusable workflows | High | Farms need delegation; certifiers need bounded access; offline work makes stale grants likely; failure leads to security or usability collapse | Use relationship+ABAC hybrid (Zanzibar + NIST ABAC); enforce explicit combining semantics (XACML-style); design revocation as first-class (RFC 7009-style endpoint semantics when tokenised); require decision traces for audit |
| Evidence system degenerates into attachments without sufficiency logic (“PDF theatre”) | High | Compliance requires defensible evidence, not just files; absence of sufficiency logic leads to inconsistent audits | Model evidence sufficiency like assurance cases (SACM); enforce chain-of-custody expectations for evidence capture/handling (NIST IR 8387; ISO/IEC 27037); keep DocumentAssembly separate from truth; provide portable attestation formats later (VC/JWS) |
| Offline UX silently commits stale or ambiguous state | High | Field capture is where uncertainty is highest; silent commits destroy trust and produce later disputes | Use explicit draft→commit workflow (ODK/Kobo “store then upload/finalise”); surface freshness and basis; constrain auto-merge to draft layer (CRDTs) and require governance gates for promotion |
| AI assistance causes silent truth mutation or over-trust | High | AI-induced hallucinations are especially dangerous in compliance contexts; if users can’t see what’s committed vs suggested, you lose accountability | Implement Amershi-style human–AI design guardrails (clear status, controllability, correction); enforce OFARM AI boundary rule via enforcement chain; keep AI outputs typed as drafts/hypotheses/advisory unless explicitly promoted |

## Actionable recommendations

1) **Formalise the TraceObject/Lot algebra as a conformance-tested core** (bounded-debt: *lot edge-case maturity*; *trace-object schema formalisation*). Use EPCIS TransformationEvent/AggregationEvent semantics as the external “reality check”; publish OFARM fixtures for split/merge/commingle/transform edge cases.

2) **Add chain-of-custody model semantics to claims/outputs** where commingling or mass-balance accounting exists (bounded-debt: *lot edge-case maturity*). Treat ISO 22095’s taxonomy as the external anchor for “what kind of mixing semantics is being claimed”.

3) **Make MaterialisationBasis explainability a hard requirement for high-consequence actions** and persist snapshots when depended upon (bounded-debt: *current-state freshness-policy deepening*). Use openEHR’s contribution/audit trail and EPCIS recordTime capture semantics as external precedents for auditable “what did we know when”.

4) **Compile PackActivationSet into an “effective context snapshot” artefact** with deterministic merge traces (bounded-debt: *template-merge validator maturity*). Use FHIR snapshot-vs-differential as a conceptual analogue; ship normative validation artefacts (SHACL/JSON Schema).

5) **Treat SemanticPathAlias like a governed canonical resource** (bounded-debt: *alias-stability governance*). Require version-pin semantics inspired by FHIR canonical URLs and explicit aliasing/lineage inspired by openEHR identification. Add automated alias-resolution regression tests.

6) **Adopt a relationship+ABAC hybrid authorisation kernel with explicit policy composition semantics** (bounded-debt: *deeper conformance at scale* for authorisation tests). Use Zanzibar as the scaling reference, NIST ABAC as conceptual foundation, and XACML combining algorithms as “composition precedent”.

7) **Constrain offline auto-merge to draft layer only** (bounded-debt: *deeper conformance at scale* for sync tests). Use CRDTs for local draft convergence if needed, but enforce that compliance truth promotion requires sync-time gating and revalidation of authority/context/freshness.

8) **Implement evidence sufficiency as a compilable structure, not a checklist** (bounded-debt: *trace-object schema formalisation*). Align evidence policies with assurance-case structures (SACM) and chain-of-custody best practices (NIST IR 8387 / ISO 27037).

9) **Evolve the Capability Manifest into a verifiable ecosystem interface** (bounded-debt: *capability-manifest ecosystem maturity*). Copy the *function* of FHIR CapabilityStatement and OpenAPI/WoT Thing Descriptions: machine-readable, deployment-specific, testable declarations tied to registry state.

10) **Ship conformance tooling as part of the standard, not as platform code** (bounded-debt: *deeper conformance at scale*). Take EPCIS as a precedent for publishing normative artefacts (schemas, shapes, OpenAPI) alongside prose; take SHACL as the formal validation anchor for RDF/graph constraints.

## Annotated bibliography

### Identity, lots, lineage, and chain-of-custody
- ★ Decisive: EPCIS Standard 2.0 () — normative semantics for aggregation, transformation, eventTime/recordTime, and validation artefacts.
- ★ Decisive: ISO 22095 () — taxonomy and requirements framing for chain-of-custody models under mixing and claims.
- PROV-O () — cross-domain provenance backbone for entity/activity/agent and derivation.

### Truth, temporality, event sourcing, and governed projections
- ★ Decisive: Fowler on Event Sourcing — clear conceptual baseline for rebuildable state from event log.
- ★ Decisive: CQRS (Greg Young; Fowler commentary) — separation of write/read models; warns about complexity, which is relevant for OFARM’s governed materialisation stance.
- Snodgrass, *Developing Time-Oriented Database Applications in SQL* — foundational temporal modelling and design discipline.
- SQL:2011 temporal features (system/application time) via vendor/summary sources — practical precedent for bitemporal discipline.

### Packs, profiles, artefact governance, and merge determinism
- ★ Decisive: FHIR profiling (differential vs snapshot) and CanonicalResource versioning — demonstrates how constraint composition becomes an ecosystem contract.
- FHIR CRMI IG — lifecycle management and repository ecosystem for computable artefacts.
- openEHR archetype identification — explicit treatment of stable IDs, aliasing, lineage, and integrity for knowledge artefacts.
- OSGi module layer — strict dependency/activation discipline as a runtime modularity analogue.
- SHACL — formal graph constraint language for validation; valuable for pack/template merge validators.

### Authority, delegation, policy, revocation
- ★ Decisive: Zanzibar paper () — relationship-based authorisation at global scale.
- ★ Decisive: NIST SP 800-162 () — ABAC definitions and considerations.
- XACML 3.0 () — policy composition via combining algorithms; useful analogue for deterministic merge law.
- OPA/Rego — policy-as-code reference implementation approach.
- Macaroons — decentralised delegation credentials with caveats; relevant for offline attenuation patterns.
- RFC 7009 token revocation () — concrete revocation primitive.

### Query semantics, path systems, planning IR
- ★ Decisive: SPARQL 1.1 Query and property paths — graph-pattern semantics + path succinctness.
- ★ Decisive: openEHR AQL — archetype-aware querying with path syntax.
- ISO/IEC 39075 GQL — property graph query standardisation signal.
- Apache Calcite paper — query planning/optimisation with semantic-preserving rewrites across heterogeneous sources.
- FHIRPath — path-based navigation and invariants; shows why path tooling/validation is essential.

### Evidence, attestation, and trustworthy AI-assisted workflows
- ★ Decisive: SACM — formal metamodel for claims/arguments/evidence (assurance cases).
- NIST IR 8387 — digital evidence preservation and chain-of-custody considerations.
- ISO/IEC 27037 — guidelines for identification/collection/acquisition/preservation of digital evidence.
- VC Data Model 2.0 + JWS — portable credential model plus signature envelope; relevant for future OFARM attestations/exported submissions.
- Human–AI interaction guidelines () — evidence-based interaction guardrails for AI assistance without over-trust.
- NIST AI RMF 1.0 — risk-managed framing for trustworthy AI deployment in socio-technical systems.

### Field/offline capture architectures
- ODK — offline-capable field capture ecosystem precedent.
- KoboToolbox offline documentation — explicit device-first storage and later upload/finalisation workflow precedent.
- CRDT foundational papers — principled convergence for replicated draft-state under concurrency.

### Capability self-description and ecosystem conformance
- FHIR CapabilityStatement — machine-readable declaration of server/client behaviours and supported operations.
- OpenAPI 3.1 — standard interface description enabling discovery of service capabilities.
- WoT Thing Description 2.0 — formal model for describing interfaces/capabilities of physical/virtual “things”.
