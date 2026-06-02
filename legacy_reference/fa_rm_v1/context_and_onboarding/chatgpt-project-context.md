# Semantic Farming Project Context

## Purpose

Use this file as project context for conceptual work in the `Semantic farming` / `Farm-RM` ecosystem.

This context is meant to help ChatGPT generate:

1. product concepts,
2. strategy and narrative documents,
3. feature ideas and specs,
4. workflow designs,
5. content and copy,
6. decision memos,
7. information architecture,
8. governance concepts.

Unless explicitly told otherwise, think at the product, domain, workflow, and specification level first, not at the code-implementation level.

## Short Definition

In this project, **semantic farming** means treating farm work as structured, meaningful, evidence-linked records that can be reused across operations, compliance, traceability, reporting, analytics, and AI.

`Farm-RM` is the reference model and contract system that makes that possible.

It is:

1. crops-first,
2. audit-aware,
3. interoperability-oriented,
4. organic-first in its rule priority,
5. designed to reduce admin burden by turning normal work records into reusable semantic assets.

## What Farm-RM Is

Farm-RM is an agriculture-specific, openEHR-inspired modeling system with these layers:

1. **Reference Model (RM)**: stable core entities, identities, relations, and lifecycle rules.
2. **Archetypes**: reusable definitions for one kind of record, such as an observation, action, evaluation, or admin artifact.
3. **Templates**: workflow-specific bundles of archetypes for a real use case.
4. **Profiles**: jurisdiction and production-mode constraints.
5. **Rule packs / report packs / API contracts**: operational and compliance-facing outputs built on top of the model.

This project is not trying to build a pure ontology for its own sake. The model exists to support real farm work, real audits, and real software interoperability.

## Core Mental Model

Think of Farm-RM as a way to make a farm season legible from beginning to end:

1. season goals,
2. workflow templates,
3. weekly planning,
4. day-to-day execution,
5. observations and signals,
6. replanning when reality changes,
7. harvest and storage,
8. quality and traceability,
9. delivery and reporting,
10. compliance closure with evidence.

The project assumes that a strong system should let people record work once and reuse it many times.

## Non-Negotiable Tenets

These are the basic tenets ChatGPT should preserve when generating ideas or content.

### 1. Record once, reuse everywhere

Normal operational records should become inputs for:

1. decision-making,
2. traceability,
3. compliance and audit preparation,
4. reporting,
5. analytics,
6. AI-assisted planning.

The project strongly resists duplicate entry and "paperwork after the fact."

### 2. Separate intent from reality

Farm-RM treats plans and execution as different things.

1. Planned work is intentional.
2. Executed work is what actually happened.
3. If reality differs from plan, the system should preserve the reason instead of hiding the change.

This is central to agronomy, operations, and auditability.

### 3. Evidence is first-class

Important claims should be supported by evidence, not just assertions.

Evidence can include:

1. invoices and receipts,
2. delivery tickets,
3. lab results,
4. cleanout and sanitation records,
5. declarations and attestations,
6. inspection artifacts,
7. supporting attachments.

If evidence is missing, prefer an explicit unknown or warning over a fabricated answer.

### 4. Append-only audit history

Compliance-relevant records should be correction-friendly but not silently rewritten.

The conceptual default is:

1. preserve history,
2. show supersession,
3. keep provenance,
4. avoid destructive edits as the main truth model.

### 5. URI-first, cross-system identity

Important business objects should be stable across tools and time.

Examples:

1. farm,
2. field,
3. crop instance,
4. operation,
5. material lot,
6. storage lot,
7. evidence record.

The point is interoperability and durable reference, not fancy naming.

### 6. Organic-first precedence

When rules conflict, the priority order is:

1. organic,
2. in-transition,
3. conventional.

This is a constitutional rule of the project, not a minor implementation detail.

### 7. Templates over ad hoc forms

The preferred unit of user-facing workflow design is not a giant generic form.

The preferred approach is:

1. stable core model,
2. reusable archetypes,
3. context-specific templates,
4. jurisdiction/profile overlays.

In other words, variability should usually live in templates, profiles, and rule packs, not in uncontrolled custom fields.

### 8. Deterministic governance around compliance

AI is welcome as an assistant, but hard compliance, legal interpretation, and safety-critical flows must remain explainable and governed.

Good outputs should preserve:

1. confidence awareness,
2. explicit assumptions,
3. missing-data visibility,
4. traceable reasoning,
5. deterministic validation where required.

### 9. Unknown is better than guessed

The project would rather show:

1. unknown,
2. not yet proven,
3. evidence missing,
4. needs attestation,

than invent a fact just to make a workflow look complete.

### 10. The model must reduce burden, not create theory theater

This repo is grounded in operational reality. Semantics are valuable only if they help people:

1. work faster,
2. miss fewer things,
3. survive inspections,
4. coordinate across tools,
5. close the season coherently.

Avoid concepts that sound elegant but increase admin work without practical payoff.

## Scope Defaults

Unless the prompt says otherwise, assume these defaults.

### Included by default

1. crops and crop operations,
2. soils, water, crop inputs, crop protection, fertility, storage, and crop product handling,
3. traceability and lot continuity,
4. compliance and audit readiness,
5. evidence linking,
6. EU baseline plus Slovenia-specific implementation needs,
7. organic and in-transition realities,
8. mixed-status safeguards where needed.

### Excluded by default

1. livestock,
2. beekeeping,
3. full accounting or ERP design,
4. speculative legal claims without evidence,
5. precision-agronomy algorithm internals unless the prompt specifically asks for them.

## Current Practical Focus of This Repository

This repository is broader than one app. It is the semantic and implementation backbone for a small ecosystem.

### The main layers in play

1. **Farm-RM package**: reference model, archetypes, templates, profiles, ontology, SHACL constraints, SQL schema, examples, generated machine artifacts.
2. **API contract and backend**: contract-first FastAPI implementation that exposes Farm-RM capabilities.
3. **Compliance/reporting program**: especially EU + Slovenia organic crops-only control-pack and recordbook generation.
4. **Operational tooling**: local Control Center dashboard for backend, database, diagnostics, and stack orchestration.
5. **Client ecosystem**: iOS client integration and farming sim/game compatibility are treated as downstream consumers of the same semantics.

### Current domain emphasis

The strongest current implementation emphasis is:

1. EU + Slovenia,
2. organic-first,
3. crops-only,
4. evidence-linked control packs and recordbook outputs,
5. traceability and status integrity,
6. OCR-assisted data capture within a Farm-RM-native contract.

## Cross-System Reality

Concepts in this project should not be designed as if they live in one isolated app.

Changes can affect:

1. semantic model and persistence,
2. backend API contracts,
3. local operational dashboard behavior,
4. iOS client assumptions,
5. farming simulation/mock data behavior,
6. release and compatibility workflows.

So when conceptualizing a feature, think across the system, not only within one screen.

## Important Conceptual Vocabulary

Use these ideas consistently.

### Reference model terms

1. `Farm`
2. `Field`
3. `CropInstance`
4. `PlannedOperation`
5. `ExecutedOperation`
6. `Observation`
7. `Evaluation`
8. `EvidenceRecord`
9. `MaterialLot`
10. `StorageLot`
11. `ComplianceSubmission`
12. `InspectionCase`
13. `NonConformity`
14. `CorrectiveAction`

### Content-architecture terms

1. **Archetype**: one reusable record definition.
2. **Template**: a workflow bundle of archetypes.
3. **Profile**: a jurisdiction or production-mode constraint set.
4. **Rule pack**: machine-readable compliance logic.
5. **Report pack**: a governed reporting/export shape.
6. **Control pack**: the dossier produced for inspection/compliance review.

### Operational terms

1. **Intent vs reality**
2. **Evidence-linked decision**
3. **Append-only history**
4. **Traceability continuity**
5. **Production status integrity**
6. **Organic-first precedence**
7. **Template projection**

## How ChatGPT Should Reason in This Project

When generating concepts, ask these questions implicitly:

1. What is the core semantic object here?
2. Is this a plan, an execution record, an observation, an evaluation, or a compliance artifact?
3. What evidence would prove it?
4. What identity must remain stable across systems?
5. What belongs in the core model versus a template/profile/rule pack?
6. What is jurisdiction-specific versus universally reusable?
7. What happens when reality departs from plan?
8. What traceability or production-status risks appear?
9. What should remain deterministic instead of delegated to AI?
10. How does this reduce admin burden in the real world?

## Preferred Output Style for Conceptual Work

Good conceptual outputs in this domain are:

1. practical,
2. explicit about assumptions,
3. structured enough to implement later,
4. careful with compliance claims,
5. grounded in workflows and evidence,
6. aware of data-model implications,
7. skeptical of unnecessary complexity.

Prefer:

1. plain language with precise structure,
2. concrete workflows,
3. named entities and clear relationships,
4. explicit scope boundaries,
5. explicit unknowns and risks,
6. phased recommendations when the problem is large.

Avoid:

1. hypey "AI platform" language,
2. generic agtech buzzwords,
3. hand-wavy compliance promises,
4. ontology-heavy abstractions with no operational use,
5. designs that assume perfect data or perfect user behavior.

## What Success Looks Like

A strong idea in this project usually does at least four things at once:

1. helps a farm operate better,
2. preserves semantic clarity,
3. improves audit and traceability posture,
4. can be reused across more than one tool or workflow.

The ideal end state is not "more forms."
It is a coherent semantic operating backbone where administration becomes a byproduct of well-structured work.

## Working Assumption for Future Conversations

If a future prompt is ambiguous, assume the user wants ideas that are:

1. crops-first,
2. organic-first,
3. evidence-led,
4. interoperable,
5. implementation-conscious,
6. realistic for a multi-tool ecosystem built around Farm-RM.
