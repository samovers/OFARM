# OFARM Advisory Scenario Workspace and Bridge Note v0.2

Date: 2026-04-24  
Status: active companion artifact  
Scope: define the smallest reusable pattern for a native Advisory-Twin scenario workspace over the active OFARM substrate without creating a second truth store, a hidden semantic fork, or a second query model, while leaving the narrow active BridgeCandidate handoff separately promoted by accepted RFC and clarifying the bounded place of ephemeral analysis sandboxes

---

## 1. Purpose

The active OFARM baseline already fixes the major architectural law:
- one semantic substrate,
- two logical twins,
- Advisory may hold scenarios, hypotheses, simulations, and competing candidate interpretations,
- Compliance may not be mutated directly by Advisory outputs,
- high-consequence use must obey basis, freshness, and governed-bridge rules.

What is still missing is the reusable pattern for **where scenarios live**, **how they bind to the substrate**, and **how they re-enter governed OFARM paths without silently becoming truth**.

This note makes that pattern explicit.

It does **not**:
- add economics to constitutional core,
- create a new top-level event family,
- create a new commit class,
- or promote scenario contracts to accepted RFC status by itself.

---

## 2. Core stance

### 2.1 Separated in authority, not separated semantically
The scenario workspace is native to OFARM and runs over the same semantic substrate.

It is separated from authoritative truth by:
- twin policy,
- bridge rules,
- freshness policy,
- publication discipline,
- and enforcement-gate discipline.

It must **not** become a detached semantic island.

### 2.2 Scenario work is Advisory by default
Scenario modeling, simulation, what-if comparison, sensitivity analysis, rolling forecast comparison, and alternative candidate interpretation belong in the Advisory Twin by default.

### 2.3 No direct mutation of Compliance or authoritative current state
Scenario outputs may:
- inform human decisions,
- request more evidence,
- create review prompts,
- generate draft bridge candidates,
- generate advisory reports or dossiers.

Scenario outputs may **not** directly:
- create or mutate compliance facts,
- create accepted executed intervention consequences,
- rewrite accepted structural state,
- bypass evidence or review law.

### 2.4 Scenario workspace is a runtime/workspace pattern, not yet a constitutional artifact-family expansion
Until spike evidence proves a stable reusable cross-deployment contract, scenario-workspace contracts remain:
- companion-level/runtime guidance,
- packizable,
- implementation-testable,
- but not yet a new constitutional artifact family.

---

## 3. What the scenario workspace is

A scenario workspace is the governed Advisory environment in which OFARM can:
- assemble scenario basis from canonical truth,
- attach assumptions and optional imported fact extracts,
- run comparison or simulation logic,
- produce advisory outputs and scenario outputs,
- preserve explicit uncertainty and provenance,
- and optionally prepare bridge candidates for later human-governed action.

It is therefore:
- native to OFARM runtime,
- query/view/output disciplined,
- refreshable and traceable,
- and deliberately non-authoritative by default.

---

## 4. What the scenario workspace is not

It is **not**:
- a second semantic store,
- a second accounting truth store,
- a report mart promoted to authority,
- a free-form notebook that can write around the enforcement chain,
- a side-channel query engine that bypasses QuerySpecification / QueryPlanIR,
- a place where AI-generated scenarios quietly become harder truth by convenience.

### 4.1 Ephemeral analysis sandbox is allowed only as bounded runtime
The rejection of “a free-form notebook that can write around the enforcement chain” does **not** forbid an ephemeral analysis sandbox.

A deployment may expose a bounded runtime where:
- a user and/or model writes code,
- authorized OFARM inputs are mounted read-only,
- scratch files and derived datasets are writable only inside a session-local workspace,
- plots, summaries, ranked alternatives, and draft advisory artifacts are produced.

That runtime remains acceptable only if it does **not**:
- bypass QuerySpecification / QueryPlanIR for new retrieval,
- hold direct authoritative write credentials,
- persist hidden current-state truth outside governed OFARM paths,
- silently promote outputs into Compliance or publication.

If retained at all, sandbox outputs should resolve into already-governed homes such as advisory outputs, BridgeCandidate, ReportAssembly/DossierAssembly, or bounded LocalArtifact support records where appropriate; the running sandbox itself remains a runtime/workspace concern, not a new constitutional artifact family.

---

## 5. Minimum workspace objects

This note keeps the object set small:
- `ScenarioSpec`
- `ScenarioResultSet`
- `BridgeCandidate`
- `ImportedFactExtract`
- `AllocationBasisDeclaration`

The broader workspace object family remains **candidate runtime contracts** until promoted later by evidence. The narrow BridgeCandidate handoff contract has now been promoted separately by `02_accepted_rfcs/OFARM_BridgeCandidate_Closure_RFC_v0_1.md`; the remaining objects still stay candidate/runtime-level here.

### 5.1 ScenarioSpec
A governed scenario definition describing at minimum:
- scenario identifier,
- target twin,
- anchor scope,
- evaluation time policy,
- ContextSnapshot reference where relevant,
- scenario objective / decision class,
- basis references,
- assumptions,
- method/model identifier,
- expected output class.

### 5.2 ScenarioResultSet
A traceable output collection describing at minimum:
- source ScenarioSpec,
- generated-at time,
- freshness posture,
- output metrics or ranked alternatives,
- explicit uncertainty posture,
- explicit evidence-class posture of contributing inputs,
- explanation / driver summary where relevant.

### 5.3 BridgeCandidate
A typed advisory object that proposes a governed next step, such as:
- request additional evidence,
- create a review task,
- prepare a draft ReportAssembly or DossierAssembly,
- prepare a draft operation plan,
- prepare a draft submission package.

A BridgeCandidate is never an accepted consequence.

### 5.4 ImportedFactExtract
A bounded external-fact object used by scenarios, such as:
- settlement summary,
- invoice-line summary,
- energy-cost summary,
- payroll summary by class,
- contractor-rate extract.

ImportedFactExtract is not canonical truth by itself and must not grow ledger semantics.

### 5.5 AllocationBasisDeclaration
Required whenever a scenario uses allocation rather than direct observation.
It declares at minimum:
- allocation driver,
- method/rule version,
- scope,
- exclusions,
- confidence posture.

---

## 6. Hard guardrails added after hostile review

### 6.1 ScenarioSpec must not become a second query language
ScenarioSpec may reference:
- saved views,
- QuerySpecification identifiers,
- basis refs,
- scope/time policy,
- and method/model identifiers.

ScenarioSpec must **not** embed a second canonical retrieval language or hide graph-pattern semantics inside scenario-only fields.

### 6.2 Result sets are not current state
ScenarioResultSet is an advisory output object.
It is never a CurrentStateMaterialization and must not be presented as one.

### 6.3 BridgeCandidate is human-gated by default
A bridge candidate must default to human-gated progression.
Low-friction “approve all” behavior is hostile to OFARM’s bridge law and should be treated as a design smell.

### 6.4 ImportedFactExtract stays extract-shaped
If someone asks for account hierarchies, journal correction workflow, reconciliation state, or close-process semantics here, the answer is no.

---

## 7. Basis, context, and freshness

Every meaningful scenario output should remain traceable to:
- substrate identifiers where relevant,
- MaterializationBasis where current state was relied upon,
- ContextSnapshot where context materially governed interpretation,
- pack/profile context where packized behavior matters,
- imported fact extracts where external inputs mattered.

Scenario outputs may tolerate staleness for exploratory viewing.
They may not silently remain in use for high-consequence export or bridge actions when basis or context has drifted materially.

---

## 8. Bridge law

The required bridge posture is:
1. scenario output or bridge candidate exists in Advisory,
2. a human or otherwise explicitly authorized actor chooses a governed next step,
3. that next step enters the normal EnforcementChain,
4. only the accepted result of that path may change authoritative current state.

A bridge path may produce:
- draft assertions,
- review requests,
- EvidenceEvents or EvidenceRecords,
- draft DocumentAssemblies,
- draft submissions.

A bridge path may not automatically produce:
- compliance fact,
- accepted executed intervention consequence,
- attested document,
- pack activation,
- human-governed decision outcome.

---

## 9. Query, view, and output posture

Query discipline remains unchanged.
Scenario work still resolves retrieval through:
- QuerySpecification,
- QueryPlanIR,
- governed execution,
- ViewModule shaping.

Where deployments offer code-interpreter-style analysis, the compute step should run over a governed read bundle or result slice produced by that normal query/materialization path.
No separate BI query semantics or direct backend truth path should appear.

Live scenario comparison should usually remain a view concern first.
Frozen decision packets should become ReportAssembly, DossierAssembly, or SubmissionAssembly where appropriate.

---

## 10. Promotion posture

This note is small enough for companion-artifact discussion because it clarifies already-set twin/bridge/materialization law.

This note still does **not** promote the full scenario-workspace contract family.
The narrow BridgeCandidate handoff is now promoted separately by `02_accepted_rfcs/OFARM_BridgeCandidate_Closure_RFC_v0_1.md`, while the remaining scenario-workspace contracts remain implementation/conformance candidates until later evidence proves they deserve broader RFC and machine-contract status.
