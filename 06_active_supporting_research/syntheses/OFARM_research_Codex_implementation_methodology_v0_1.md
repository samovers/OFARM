# Implementing OFARM with Codex without semantic drift or brittle enforcement

> Source note (migration cleanup, 2026-04-10): This report preserves a prior Deep Research synthesis. Inline web/file citation markers were removed during packaging cleanup because their source handles were not portable into the migrated project. Treat the report as supporting research and re-verify external claims before promoting any recommendation into active law.

## Failure mode catalog

### Risk scale used
Severity: **Critical / High / Medium / Low**. Likelihood: **High / Medium / Low** (conditional on typical AI-assisted development practices).

The catalog is written specifically against OFARM’s constitutional surfaces (truth/authority/state/event/pack/query/output law) and the platform’s enforcement-chain posture.

### Semantic integrity and truth-law breakage
These are the “silent corruption” class: the system appears to work, but becomes untrustworthy (especially across long horizons, packs, or audits).

- **Projections become hidden truth stores** (e.g., a read model, cache, index, “convenience table”, or edge store starts accepting writes or becomes the de facto authority).
  Severity: **Critical**. Likelihood: **Medium–High** in early builds if performance pressure exists.
  Why dangerous for OFARM: directly violates the “assertion/history-first authority + governed current-state materialisation” split and undermines traceability and audit.

- **AI-generated shortcut paths that bypass EnforcementChain gates** (e.g., code paths that “just write the record” without authority/validation/evidence/review/materialisation gates).
  Severity: **Critical**. Likelihood: **Medium** unless you enforce gate coverage mechanically.
  OFARM-specific: the platform architecture explicitly requires authoritative outcomes to cross the relevant gates; bypassing creates “fake conformance”.

- **Current-state materialisation used as deeper truth** (developers treat a materialised snapshot as the authority instead of a derived view with basis/freshness).
  Severity: **Critical**. Likelihood: **Medium** (a common optimisation trap).
  OFARM-specific: breaks auditability (missing MaterialisationBasis) and introduces stale-state safety hazards in high-consequence flows.

- **Event consequences applied without governed acceptance** (events start mutating compliance state “because the event exists”).
  Severity: **Critical**. Likelihood: **Medium**.
  OFARM-specific: violates “event is not automatically current state” and collapses commit/promotion law (operation claim ≠ accepted executed consequence).

- **Evidence sufficiency silently weakened** (e.g., evidence checks skipped for some flows; “advisory outputs” treated as satisfying evidence).
  Severity: **Critical**. Likelihood: **Medium**.
  OFARM-specific: directly violates the advisory/compliance boundary and promotion safety rule (default is “do not auto-promote”).

- **Twin contamination** (Advisory-Twin hypotheses leak into Compliance-Twin current state, or “bridge” becomes implicit).
  Severity: **Critical**. Likelihood: **Medium**.
  OFARM-specific: breaks the one-substrate/two-policy twin architecture and creates governance bypass in the most sensitive surface.

### Pack/profile merge and semantic surface corruption
Any merge bug here becomes system-wide because packs are a context-defining layer, and OFARM requires deterministic merge traces.

- **Pack merge implemented incorrectly for a surface family** (wrong merge mode chosen; illegal merge allowed; conflict should hard-fail but silently composes).
  Severity: **Critical**. Likelihood: **Medium**; AI codegen increases “looks plausible” merges.
  OFARM-specific: pack overlap rules are constitutional; determinism and trace are required (PackMergeResolutionTrace).

- **Template/schema drift across packs** (multiple packs “agree” informally but schemas diverge; intersections not monotone).
  Severity: **High–Critical**. Likelihood: **Medium–High** in multi-pack deployments.
  OFARM-specific: template constraints have specific merge law; drift breaks alias stability and query contracts.

- **Undeclared touched surfaces** (pack touches authority rules, evidence policy, or event subtypes without declaring it).
  Severity: **High**. Likelihood: **Medium**.
  OFARM-specific: violates “touched surfaces must be declared” and enables stealth semantic override.

- **Activation partial success** (runtime installs/activates some artifacts and silently ignores others due to conflict).
  Severity: **High–Critical**. Likelihood: **Medium** unless you enforce deterministic fail semantics.
  OFARM-specific: incompatible PackActivationSet must fail deterministically with trace, not “best effort”.

### Authority, delegation, and governance bypasses
In governance-heavy systems, authorisation bugs are not “security bugs” only; they are semantic integrity bugs.

- **Silent authority bypasses** (missing default-deny; broad role implies action class; derived-scope implied).
  Severity: **Critical**. Likelihood: **Medium**.
  OFARM-specific: authority is action-class based with default deny and explicit scope inheritance modes; implicit grants invalidate auditability.

- **Delegation exceeds delegator authority** (insufficient checks; stale edge grants).
  Severity: **Critical**. Likelihood: **Medium**.
  OFARM-specific: delegation must be bounded and traceable; offline sync must re-check authority at commit.

- **Non-human actions accidentally permitted in human-governed classes** (review accept, pack activation, attestation).
  Severity: **Critical**. Likelihood: **Medium** if automation is overused.
  OFARM-specific: v2 posture is explicitly human-governed by default for those actions.

- **Audit traces become non-authoritative or lossy** (AuthorizationDecisionTrace missing critical basis; enforcement logs incomplete).
  Severity: **High**. Likelihood: **Medium**.
  OFARM-specific: governance requires durable, explainable traces for decisions and merges.

### Freshness, time, and state hazards
In OFARM, time is multi-dimensional and fresh materialisation is purpose-sensitive.

- **Stale current state used in high-consequence flows** (or stale treated as acceptable due to UI convenience).
  Severity: **Critical**. Likelihood: **Medium** (a common production regression).
  OFARM-specific: high-consequence use requires FRESH recomputation or refusal/routing; freshness is purpose sensitive and must be explainable.

- **Temporal collapse** (event time / record time / assertion time conflated; migrations “fix dates”).
  Severity: **High–Critical**. Likelihood: **Medium** (especially with AI refactors).
  OFARM-specific: multi-temporal law is core; collapsing breaks audit and correct supersession behaviour.

- **MaterialisationBasis cannot be reconstructed** (derived state computed but basis not stored or basis identifiers rot).
  Severity: **High–Critical**. Likelihood: **Medium**.
  OFARM-specific: basis trace is necessary for trust, especially for DocumentAssemblies and high-consequence reliance.

### Query, alias, and contract drift
AI coding makes it easy to “just add a helper query”, which is precisely how query contracts erode.

- **Alias-resolution drift** (SemanticPathAlias resolves ambiguously; fallback “best guess”; version pinning omitted).
  Severity: **High**. Likelihood: **Medium–High** unless enforced.
  OFARM-specific: alias resolution must be governed and version-stable; ambiguous should fail, not guess.

- **QueryPlanIR becomes a hidden semantics layer** (planner embeds meaning beyond formal schema; meaning differs by execution target).
  Severity: **High–Critical**. Likelihood: **Medium**.
  OFARM-specific: QuerySpecification → QueryPlanIR must preserve semantic equivalence and stay governed enough to prevent hidden meaning.

- **Internal query contracts violated by “helpful” optimisations** (planner shortcuts across projections without trace-back; different results admitted).
  Severity: **High**. Likelihood: **Medium**.
  OFARM-specific: projection rule requires traceability back to canonical truth; equivalence must hold across targets for conformance.

### Offline sync, concurrency, and idempotency bugs
These are catastrophic because they create non-local corruption and are hard to reproduce.

- **Edge draft graph becomes quasi-authority** (edge finalises outcomes it shouldn’t; later sync “reconciles” by overwriting).
  Severity: **High–Critical**. Likelihood: **Medium**.
  OFARM-specific: edge is offline-capable but core is online-authoritative; final compliance facts and attested outputs are not edge-final by default.

- **Idempotency failures and duplicate commits** (retry creates multiple AssertionRecords or consequences; merge semantics flawed).
  Severity: **High**. Likelihood: **Medium**.
  OFARM-specific: append-only history tolerates duplicates poorly because later materialisations and audits amplify them.

- **Concurrent pack activation / context snapshot mismatch** (materialisation computed under context A but labelled as context B).
  Severity: **High**. Likelihood: **Medium**.
  OFARM-specific: materialisation identity includes context snapshot; mismatch breaks explainability and safety.

### Security and supply-chain regressions amplified by agents
AI tools change the attack surface: prompt injection, tool abuse, and unsafe automation.

- **Prompt injection via repo content to hijack an agent** (e.g., malicious instructions in README, issues, tests, or generated diffs).
  Severity: **Critical**. Likelihood: **Medium–High** with autonomous agent modes.
  Evidence: systematic analysis frames prompt injection as architectural vulnerability needing defense-in-depth, not ad hoc filters.

- **Agent tool abuse / command execution risk** (LLM agent runs destructive commands, exfiltrates secrets, or modifies settings).
  Severity: **Critical**. Likelihood: **Medium**; rises with “always allow” configurations.
  Evidence: public incident class “IDEsaster” and similar reporting show real exploit chains affecting AI-assisted IDEs; OpenAI guidance emphasises sandboxing, approvals, and least privilege for agent tools.

- **Security regressions from AI-generated code** (insecure defaults, missing input validation, unsafe crypto, auth mistakes).
  Severity: **High–Critical**. Likelihood: **High** without security-specific gating.
  Evidence: controlled and large-scale studies find increased insecurity and overconfidence when using LLM coding assistance in security tasks, plus vulnerability prevalence in model outputs.

### Process and socio-technical failure modes (the ones that actually kill architecture)
Even with perfect tests, these destroy OFARM by gradual erosion.

- **Spec drift between docs and code** (architecture texts remain aspirational; code and fixtures become de facto spec).
  Severity: **High–Critical**. Likelihood: **High** unless you build “spec-as-code” enforcement.
  Evidence: architecture drift/erosion is a known industrial phenomenon and requires explicit countermeasures.

- **Architecture erosion via “just this shortcut” acceptance** (local optimisations violate prescriptive architecture).
  Severity: **High**. Likelihood: **High** under delivery pressure.
  Evidence: drift and erosion are well-studied; prevention usually requires both tooling and process discipline.

- **Flaky or shallow tests and fake conformance** (tests validate only happy paths; conformance suites exist but not enforced).
  Severity: **High**. Likelihood: **Medium–High** when AI writes tests that mirror implementation.
  Evidence: mutation testing literature treats mutant survival as a signal that tests are weak; mutation testing correlates with improved practices and fault coupling.

- **Poor review discipline for generated code** (large diffs; reviewers rubber-stamp).
  Severity: **High**. Likelihood: **High** at scale.
  Evidence: modern code review empirics show reviews often focus less on defect finding than teams expect; tooling and decomposition of change matter.

- **Irreproducible agent behaviour** (model updates, nondeterminism, context truncation changes patches between runs).
  Severity: **High**. Likelihood: **High** unless you pin versions and capture artefacts.
  Evidence: evaluation work stresses reproducibility and harness design; SWE-bench moved to containerised evaluation to improve reproducibility.

- **Technical debt accumulation from AI-assisted commits** (duplication, churn, shallow abstractions; long-horizon maintainability loss).
  Severity: **High**. Likelihood: **Medium–High**.
  Evidence: a large-scale empirical study (March 2026) reports on technical debt in “verified AI-authored commits” across many repos and assistants.

## Best-practice findings from papers and technical literature

### What is strongly supported
**Formalising the hard parts early reduces catastrophic bugs, especially in distributed/stateful systems.**
Experience reports from mission-critical distributed systems show that writing formal specifications and model checking (notably with TLA+) helps prevent “serious but subtle bugs” before they hit production.
This maps directly onto OFARM’s highest-risk mechanisms (pack merge determinism, current-state freshness/invalidation, authority/delegation semantics, offline sync/idempotency).

**Code review works best as a socio-technical control when changes are small and comprehensible.**
Empirical study of modern code review finds that although defect detection is a primary motivation, outcomes are often broader (knowledge transfer, improved solutions), and that the ability to understand/decompose changes is a key review challenge.
For AI-generated code, this implies you must force small, scoped diffs with explicit intent, otherwise review becomes theatre.

**Property-based and model-based testing uncover edge cases that example-based unit tests systematically miss.**
QuickCheck’s founding work demonstrates the effectiveness of property-based random testing and highlights pitfalls; model-based testing surveys describe how tests generated from models can automate validation with oracles.
For OFARM, “properties” can encode constitutional invariants (monotone constraint intersection, default-deny authorisation, determinism of pack merge outcomes, idempotent sync).

**Mutation testing can identify weak test suites and is coupled with real faults.**
Work on mutation testing practices provides evidence that mutation testing drives stronger tests and that mutants are coupled with real faults in empirical analyses.
This matters because AI-written tests often overfit to the implementation rather than the spec.

**AI coding tools measurably improve speed, but security and correctness risk rises without strong validation and oversight.**
Controlled experiments show productivity improvements (faster completion) with AI pair programmers.
In contrast, security-focused user studies and analyses find that AI assistance can lead to less secure code and increased overconfidence, and systematic investigations find insecure suggestions under common prompts.
The implication is structural: speed gains must be paid for with governance, gating, and verification—especially for OFARM’s governance-heavy surfaces.

### What is promising but immature
**LLM coding agents can solve repo-level tasks when harnessed with tool interfaces and rigorous evaluation harnesses**, but reliability varies and is harness-dependent. SWE-agent shows how agent-computer interface design improves performance on repo-level benchmarks, and SWE-bench provides a realistic evaluation framework.
For OFARM, this suggests agents can help implement well-scoped modules, but only within a workflow that preserves reproducibility, constraints, and reviewability.

**Systematic work on code hallucinations is converging on mitigation patterns**, but it remains an active area. A 2025 systematic review of code hallucinations synthesises causes and mitigation strategies (constrained decoding, post-checking, program analysis, testing).
Practical takeaway: always assume “plausible but wrong” exists, and force external verification (schemas, compilations, property tests, fixtures).

**Agent security guidance is improving quickly, but the ecosystem is still brittle.**
Prompt injection against agentic coding assistants is increasingly treated as an architectural vulnerability class that needs defense in depth.
OpenAI’s agent-safety guidance emphasises structured outputs, not injecting untrusted variables into high-priority instruction channels, sandboxing, allowlists, and human approvals for risky actions.
Net: you can operate agents safely, but only if you treat them as privileged automation with strict boundaries.

### What is hype or weakly supported
**“Let the agent build the architecture end-to-end”** is not supported for governance-heavy systems. Repo-level benchmarks show progress, but also highlight the importance of harness design, reproducibility controls, and robust evaluation.
For OFARM, any approach that relies on the model “remembering the constitution” across weeks of work is structurally fragile.

**“AI-generated tests are enough”** is weak. Without mutation/property/model-based pressure, AI tests often validate the implementation, not the invariant. The mutation testing literature treats test strength as a measurable engineering concern, not a vibes issue.

## Recommended implementation methodology for OFARM with Codex

This is a concrete methodology designed to make semantic drift mechanically difficult and to keep every change auditable and reversible.

### Project organisation model
**Use a “constitutional kernel + generated perimeter” architecture in the repository.**

- **Constitutional kernel**: small, hand-curated modules that encode the non-bypassable invariants (enforcement chain gate interfaces, authority evaluation core, pack merge resolver core, materialisation basis/freshness core, QuerySpecification/QueryPlanIR validators). This layer should be deliberately boring and maximally testable.
  Rationale: this is where bugs are catastrophic and difficult to fix retroactively; treat it like the “trusted computing base”.

- **Generated perimeter**: higher-volume code that Codex can help with safely when bounded: adapters, mapping modules, view shaping, CLI tooling, test-fixture generators, documentation renderers, scaffolding, and non-authoritative projections.

This matches both OFARM’s constitutional posture (platform must realise law via deterministic enforcement points, not convention) and the empirical reality that AI speedups are strongest on implementation work while correctness/security risks rise on subtle semantic work.

### Artifact order of implementation
OFARM’s most dangerous failures happen when high-level features appear before the hard constraints are executable. The safe order is the reverse:

1. **Schemas and executable contracts first**
   Implement machine-validatable schemas for: AssertionRecord, ReviewDecision, Evidence relations, Pack manifests + touched surfaces, PackActivationSet, PackMergeResolutionTrace, CurrentStateMaterialization (including MaterializationBasis and freshness), QuerySpecification, QueryPlanIR, Capability Manifest.
   OFARM explicitly requires schema validation for QuerySpecification and QueryPlanIR and enforces materialisation identity/basis/freshness; make those compile-time/CI-time failures, not runtime surprises.

2. **EnforcementChain skeleton second**
   Build the gate pipeline interfaces and enforcement logging as a “spine” before you build feature flows. OFARM defines gates (ingress normalization, authority, validation, pack applicability, evidence, review/promotion, materialisation, publication). Make every authoritative write path require traversing a typed gate pipeline.

3. **Pack merge resolver core third**
   Implement merge legality checks (surface family → allowed merge modes) and deterministic merge resolution + trace emission. Packs are a multiplier: you can’t safely add more artifacts until merge law is trustworthy.

4. **Authority/Delegation/Revocation core fourth**
   Implement action-class-based authorisation with default deny, inheritance modes, and decision traces. Then wire it into the enforcement chain.

5. **Current-state materialisation core fifth**
   Implement: basis computation, invalidation triggers, freshness evaluation (purpose-sensitive), and “high-consequence” enforcement (recompute/refuse/route). This is a safety boundary, so it must be correct before you build attestation and documents.

6. **Query compilation sixth**
   Implement QuerySpecification validation, alias resolution contract (fail on ambiguity), QueryPlanIR generation, and equivalence tests across execution targets.

7. **Only then: higher-level product flows (capture/import/views/doc assemblies)**
   Because the spine can now enforce “capture is not commit”, advisory/compliance boundaries, and publication traceability.

### Keeping docs/schemas/code/tests/fixtures aligned
The anti-drift mechanism is **bidirectional traceability plus executable conformance**:

- **Single source of truth for contracts**: schemas live centrally; both runtime validation and test fixture generation import from them. This prevents schema drift by construction.
- **Conformance suite is a first-class product**: OFARM already defines a minimum conformance baseline that includes pack merge fixtures, authority decision tests, freshness tests, alias stability tests, equivalence tests, and more. Treat that list as a release gate: no merge that reduces conformance.
- **Mutation testing on the constitutional kernel**: apply mutation testing to gate evaluation, authorisation rules, merge legality, and materialisation freshness. Mutation testing is specifically useful for detecting when tests are “happy-path theatre”.
- **ADR discipline for semantic decisions**: record each constitutional-surface decision (e.g., “what counts as monotone narrowing for TEMPLATE_CONSTRAINT merge”) as an ADR and require that PRs touching those surfaces link to an ADR. ADRs are an established lightweight architecture-knowledge practice and have been studied in practice.

### Task structuring for Codex
Codex can be extremely effective when tasks are bounded, checkable, and reversible; OpenAI’s own best-practices emphasise prompting, planning, validation, skills, and repeatable workflows via repo-local instructions.

A safe decomposition pattern for OFARM is:

- **Contract slice**: “Add/adjust schema + invariants + fixtures” (no runtime changes yet).
- **Kernel slice**: “Implement one pure function / resolver with property tests + golden fixtures.”
- **Integration slice**: “Wire into enforcement chain at one gate boundary; add trace emission tests.”
- **End-to-end slice**: “Add a single user-visible flow that exercises the gate path; add determinism replay test.”

Each slice must be small enough that a reviewer can understand it, reflecting code-review evidence that comprehension and decomposition are central.

### Managing long-horizon context loss
Long-horizon failure is a structural risk for agent systems: context gets summarised, truncated, or misconstrued. OpenAI’s own deep dive on the agent loop highlights context management as a core harness responsibility.

Mitigations that work in practice:

- **Repo-local “constitution extracts” for agents**: keep a short, canonical, versioned “constitutional kernel contract” document that agents must read first (analogous to repo-local instruction files). This reduces reliance on long conversational memory.
- **Hard boundaries on allowed files per task**: force edits to a small set of files; anything else is a new task requiring a new review context.
- **Transcript + patch provenance retention**: store the agent prompt, tool logs, and produced diff as artefacts (important for audit and for reproducing why/what happened).
- **Model pinning and “diff-first” reruns**: pin model/version for a release train; when re-running, ask for a minimal patch relative to current branch state, not a fresh rewrite.

### Making generated code auditable and reversible
The strategy is not “trust the agent”; it is “make every change easy to reason about”.

- **Always produce a PR, never direct-to-main automation** (Codex itself is positioned as proposing PRs for review).
- **Require each PR to include**: (a) changed contracts/schemas if applicable, (b) tests/fixtures, (c) trace changes (e.g., merge trace, authorisation trace), (d) migration plan if data shape changed.
- **Use “replay artefacts”**: for any high-risk logic, keep golden fixture sets that must remain stable unless an explicit constitutional change is made.

## Proposed gated workflow

This workflow is deliberately stage-gated to prevent AI speedups from becoming semantic debt.

### Stage gates and artefacts
**Gate A — Contract authoring (human-owned)**
Artefacts: schema diffs, invariant statements, ADR if meaning changes, fixture plan.
Automated checks: schema compilation, backward compatibility checks where required, “no hidden core” and “touched surfaces declared” lints (OFARM requires touched surfaces declarations).

**Gate B — Fixture authoring (human + agent)**
Artefacts: golden fixtures for conformance, including pack-merge fixtures, authority decision fixtures, freshness fixtures.
Automated checks: fixture schema validation; determinism of fixture replay.

**Gate C — Codex generation (agent-executed, constrained)**
Agent inputs: contract + fixtures + file scope + “definition of done (DoD)”.
Agent outputs: small diff + tests + update to conformance suite.
Rationale: OpenAI best practices emphasise planning and validation; you are enforcing this mechanically.

**Gate D — Automated verification (non-negotiable)**
Must pass: unit/integration tests, property-based tests, schema validation, conformance suite, static analysis, secret scanning, supply-chain checks.
Security posture: align with secure development frameworks (e.g., SSDF practices like implementing secure build/test and provenance controls).

**Gate E — Human review (two-tier)**
Tier 1: conventional code review (small diffs only).
Tier 2: “constitutional review” for sensitive surfaces (pack merge, authority, materialisation, query planning). Use a checklist similar in spirit to software inspection checklists (inspections are a longstanding effective verification method).

**Gate F — Conformance verification (release gate)**
Run the full OFARM minimum conformance baseline suites on CI nightly and on candidate releases, including equivalence, merge determinism, freshness policy tests, and authority action tests (these are explicitly listed in OFARM RC2.1).

**Gate G — Merge / release**
Rules: no auto-merge by agent; high-risk changes require explicit approvals; tag release with conformance report reference and pinned agent/model version.

### Why this workflow is anti-failure for OFARM
It turns the most dangerous classes (semantic bypass, drift, fake conformance) into **mechanical build-breakers** rather than “reviewer intuition”. This is precisely the right pattern for architecture drift/erosion countermeasures: you cannot rely on discipline alone.

## Test strategy

OFARM’s own conformance baseline already outlines what “deep conformance” means; the test strategy below translates it into a methodology that resists AI-specific brittleness (overfitted tests, hallucinated integrations, shallow fixtures).

### Schema validation as the first line of defence
- Validate all constitutional artefacts against formal schemas at build time: QuerySpecification, QueryPlanIR, pack manifests, capability manifests, materialisation records.
- Property: “no unvalidated artefact crosses a gate boundary”.

### Contract tests for enforcement gates
For each EnforcementChain gate (authority, validation, evidence sufficiency, review/promotion, materialisation, publication), build **contract tests**: given an input class, the gate must emit a deterministic outcome and trace. This maps directly to the platform requirement for deterministic enforcement points and enforcement logging.

### Property-based tests for constitutional invariants
Property-based testing is a direct fit for OFARM’s “law-like” semantics. QuickCheck’s work is foundational for expressing and testing invariants with generated inputs.

High-value properties for OFARM:

- **Pack merge determinism**: for the same PackActivationSet and inputs, merge outcome and trace are identical.
- **Merge legality**: illegal merge modes for a surface family always hard-fail (never degrade).
- **Authority default deny**: if a valid authorisation chain cannot be proven, decision is DENY; traces must include basis.
- **Freshness safety**: any high-consequence action requires FRESH materialisation under policy or refuses/routes; stale must not silently proceed.
- **Alias resolution stability**: an alias either resolves deterministically under the declared versioned contract or fails clearly (no guessing).
- **Projection non-authority**: no code path allows authoritative writes to non-canonical projections (can be tested by fault injection hooks).

### Golden fixtures for deep conformance
Golden fixtures are not “example data”; they are executable spec. OFARM’s conformance baseline explicitly calls for merge fixtures, authority fixtures, freshness fixtures, alias-resolution fixtures, and more.

Recommended fixture tiers:

- **Micro fixtures**: minimal counterexamples (e.g., two packs conflict on TEMPLATE_CONSTRAINT, must HARD_FAIL).
- **Scenario fixtures**: realistic farm/site/crop lifecycle with late-arriving evidence, supersession, and offline drafts.
- **Audit fixtures**: ensure DocumentAssembly and MaterializationSnapshot capture reconstructible basis trails.

### Mutation and differential testing to resist fake conformance
- **Mutation testing on kernel invariants**: use mutation testing to ensure tests actually fail when semantics are perturbed; empirical work supports that mutation testing improves test quality and is linked to real faults.
- **Differential testing across execution targets**: same QuerySpecification executed via graph engine vs materialisation vs derived read model must be semantically equivalent within defined tolerances; OFARM requires equivalence tests across targets.

### Replay and determinism testing
- Deterministic replay of: pack merge, authorisation decisions, materialisation basis generation, and high-consequence actions.
- Store replay artefacts for regressions (inputs + expected traces).
This directly counters irreproducible agent behaviour by making runtime semantics reproducible regardless of how code was authored.

### Offline/sync and concurrency tests
- Idempotent sync tests with retries and partial failures.
- Authority re-evaluation tests: stale grants revoked at core must invalidate edge’s ability to finalise.
- Multi-temporal tests to ensure event time vs record time vs assertion time remain distinct.

### Security/authorisation tests and agent-aware threat tests
- Action-class authorisation matrix tests (including “non-human prohibited by default” classes).
- Prompt-injection resilience tests for tooling and CI automation (treat untrusted repo content as hostile).
This aligns with the emerging view that prompt injection is a first-class architectural vulnerability.

## Codex-specific operating guidance and implementation anti-patterns

### Operating guidance that reduces bad output
OpenAI’s Codex guidance emphasises repeatable workflows (best practices, repo-local instructions, skills) and safe operation (approvals, sandboxing, network controls).

The OFARM-specific synthesis is:

- **Use repo-local instructions as “constitutional binding”**
  Maintain a short “OFARM kernel invariants” instruction file that forces every task to: (a) cite the gate boundaries it touches, (b) list the invariants it must preserve, (c) update fixtures. This mirrors Codex’s support for repo-local instruction loading.

- **Prefer narrow prompts for kernel work; allow broader prompts only for perimeter work**
  Kernel prompts should specify: exact files allowed, invariants, tests required, and explicit “what must not change”.
  Broader prompts are acceptable for: code formatting, scaffolding, docs rendering, test data generation, mapping-module boilerplate.

- **Force “tests-first diffs”**
  Ask Codex to submit fixtures/tests before implementation or at least in the same PR. This counters hallucination and “plausible-but-wrong” code generation documented in hallucination surveys.

- **Treat security as a first-class acceptance criterion**
  Empirical studies show AI assistance can lead to less secure code and overconfidence; the safe posture is to require security checks and explicit threat model notes for any change that touches authorisation, evidence, or publication.

- **Operate Codex with approvals and sandboxing; do not allow autonomous destructive actions**
  OpenAI provides guidance on agent approvals & security and recommends controls such as sandboxing, network allowlists, and human-in-the-loop for risky actions. This is directly relevant given prompt-injection risk.

- **Detect drift using conformance deltas, not conversational confidence**
  Drift signals: reduced conformance coverage, increased exceptions/fallbacks, added “temporary” bypasses, emergence of implicit semantics. Use CI to block.

- **Regenerate vs repair rule**
  If Codex produces a large diff or modifies unintended files, regenerate with a narrower scope. Repair only when the diff remains small and the tests/fixtures prove intent. This follows the general principle that review comprehension degrades with large changes.

### What not to ask Codex to do in one step
Avoid single-step tasks that combine multiple constitutional surfaces. Typical “don’t do this” bundles:

- “Implement pack activation + merge + evidence policy + query planning” in a single change.
- “Refactor the enforcement chain” while also “adding a new commit class”.
- “Optimise projections/caches” while “changing materialisation basis”.

These are precisely the scenarios where architecture erosion happens and where long-horizon context loss bites.

### Implementation anti-patterns to avoid in OFARM
This is the clear “do not do” list, targeted at governance-heavy semantics.

- **Letting any code path write authoritative state outside the canonical substrate** (including edge stores, caches, projections).
- **Adding “helpful fallbacks”** (alias resolves “best effort”; query planner substitutes meaning; merge resolver auto-composes conflicts). OFARM’s law calls for clear failure or governance-required outcomes, not silent guessing.
- **Encoding constitutional meaning in ungoverned conventions** (magic strings, undocumented precedence overrides, implicit role → action mapping).
- **Using advisory outputs as if they were promotable facts** (directly or indirectly) without explicit governed bridge.
- **Treating documentation as optional** for semantic decisions. Architecture erosion research shows drift is common without explicit maintenance mechanisms.
- **Accepting large AI-generated PRs** that cannot be meaningfully reviewed; empirics show comprehension/decomposition are central to review effectiveness.
- **Running agents with broad, persistent permissions** (shell, filesystem, network) without approvals and allowlists; prompt injection makes this an architectural risk, not a user-error risk.

## Recommended first implementation wave and annotated bibliography

### Recommended first implementation wave
The first wave should build the “semantic kernel + conformance harness” so every later feature is constrained by executable law.

**Implement first (instrument heavily):**

- **Conformance harness scaffolding**: CI that runs schema validation, conformance suites, replay tests, and publishes a conformance report artefact per build.
  Why first: it becomes your drift detector.

- **EnforcementChain spine + trace capture**: define gate interfaces, standard outcomes, and durable enforcement logs.
  Why: it prevents bypasses early.

- **Pack merge resolver core + PackMergeResolutionTrace** with golden fixtures for each surface family (VOCABULARY_BINDINGS, EVIDENCE_POLICY, TEMPLATE_CONSTRAINT, DECISION_RULE, etc.).
  Why: pack law errors have multiplicative impact.

- **Authority engine core + AuthorizationDecisionTrace** with default deny, scope inheritance modes, delegation and revocation tests.
  Why: governance correctness is non-negotiable.

- **Materialisation basis and freshness core** with explicit invalidation triggers and high-consequence enforcement tests.
  Why: stale state in high-consequence flows is a top-tier OFARM failure.

**Defer (until kernel is stable):**

- Aggressive performance optimisations (heavy derived projections, denormalised marts).
- Broad autonomous agent workflows (multi-agent refactors, automated governance-sensitive actions).
- Wide interoperability mappings that could import semantics drift (only implement mappings with strong round-trip fixtures once core is stable).

**Codex role in the first wave (safe use):**
- Use Codex to generate scaffolding, test harness setup, schema boilerplate, fixture generators, and narrow implementations with properties.
- Do not use Codex to “invent” merge semantics or authority rules; require it to implement from explicit invariant lists and fixtures, then prove via tests.

This matches the empirical pattern: AI improves throughput, but correctness and security require strong validation and oversight.

### Annotated bibliography
This bibliography is curated toward “implementation methodology under AI assistance” and “verification mechanisms that resist drift”.

- **AI-assisted coding: productivity vs risk**
  - Controlled experiment showing faster completion with AI pair programming (productivity gains).
  - User study showing less secure code and overconfidence with LLM code assistants in security tasks.
  - Systematic/empirical analysis finding insecure suggestions in AI-generated code under common conditions.
  - Large-scale empirical study (March 2026) on technical debt introduced by AI coding assistants “in the wild”.
  - Security/quality analysis of LLM-generated code across languages using static security analysis.

- **Hallucination and reliability of code generation**
  - Systematic literature review of code hallucinations: causes, mitigation strategies, evaluations.

- **Agentic software engineering and evaluation**
  - Repo-level agent interface design and performance: SWE-agent (agent-computer interfaces).
  - SWE-bench: realistic repo-level benchmark and containerised evaluation harness for reproducibility.

- **Prompt injection / agent security**
  - Systematic analysis framing prompt injection against agentic coding assistants as architectural vulnerability requiring defense in depth.
  - OpenAI agent safety guidance recommending structured outputs and avoiding injecting untrusted variables into high-priority instruction channels.
  - OpenAI Codex operational security guidance (approvals, sandboxing, network controls).

- **Formal methods for subtle semantic correctness**
  - Experience report on formal methods in critical distributed systems (TLA+ at AWS) and rationale for choosing TLA+.
  - “Industrial use of TLA+” resource hub for practice examples and adoption context.

- **Architecture erosion and keeping architecture aligned with implementation**
  - Survey of techniques to prevent/detect/repair architecture erosion.
  - Work discussing architecture drift and erosion symptoms and prevention tooling/processes.

- **Review discipline and inspection methods**
  - Empirical study on modern code review motivations/outcomes/challenges (importance of comprehension and decomposition).
  - Software inspections as an effective verification process (inspection as structured human gate).

- **Testing methods suited to “semantic law”**
  - Property-based testing foundation (QuickCheck) for executable invariants.
  - Systematic review of model-based testing approaches and model-driven testing surveys (test generation from models + oracles).
  - Mutation testing evidence linking mutants to real faults and improved test practices.

- **Codex operational documentation**
  - Codex best practices (prompting, planning, validation, workflows).
  - Repo-local instruction mechanism (AGENTS.md) and agent loop deep dive (context management as harness responsibility).
  - Codex approvals & security guidance.
