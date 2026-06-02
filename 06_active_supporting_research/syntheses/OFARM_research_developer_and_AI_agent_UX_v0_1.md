# OFARM developer experience and AI-agent experience research

> Source note (migration cleanup, 2026-04-10): This report preserves a prior Deep Research synthesis. Inline web/file citation markers were removed during packaging cleanup because their source handles were not portable into the migrated project. Treat the report as supporting research and re-verify external claims before promoting any recommendation into active law.

## Executive summary

1) **Your biggest DX risk is not “complexity”; it’s *ambiguity under pressure*.** OFARM’s baseline already rejects “hidden runtime interpretation” for critical seams (e.g., alias resolution should “fail clearly rather than guess”, and authorisation is default-deny). That stance is correct; the DX work is to make that determinism *legible*, *navigable*, and *tool-assisted* in every failure mode, not to water down the model. (OFARM Query Architecture Note v0.1, §6; OFARM Authority Policy Model RFC v0.1, §2.)

2) **Treat capability discovery as a first-class product surface (humans) and a safety boundary (agents).** OFARM’s Capability Manifest is already the right structural move (deployment self-description, capability negotiation, conformance reporting). To reach “standard-grade”, it must become the equivalent of Kubernetes discovery + OpenAPI exposure (for clients/tools) and FHIR CapabilityStatement-style discovery (for implementers), with explicit negotiation and scoped views.

3) **Error responses must be structured, stable, and “debuggable without tribal knowledge”.** For complex contract-heavy platforms, the “friendly error string” is not enough; you need machine-readable error types with pointers, plus human-facing resolution hints. RFC 9457 (Problem Details) is the baseline; Google’s AIP-193 shows how to do stable machine identifiers + metadata without forcing clients to parse strings. FHIR’s OperationOutcome shows a domain-grade pattern for multiple issues + expression pointers.

4) **Split “plan” from “execute” everywhere you can (especially for agents).** OFARM’s QuerySpecification vs QueryPlanIR split is exactly the kind of separation that reduces unsafe autonomy: agents can propose plans and humans (or policy) can authorise execution. Kubernetes’ server-side dry-run is a proven pattern: “run all validation and admission checks without mutating state.” You want OFARM equivalents for query planning, pack activation, and high-governance promotion steps.

5) **The twin model is a DX asset, if you weaponise it as a safety rail.** OFARM’s “one substrate, two logical twins” boundary plus “no fully automatic non-human promotion into compliance” is exactly the guardrail AI ecosystems need (it blocks “excessive agency” by design). The UX job is to prevent developers (and agents) from accidentally treating Advisory outputs as compliance truth, especially under deadlines. (OFARM Constitution RC2.1, §12; OFARM Platform Enforcement Architecture Memo v0.1, §8.)

6) **Packs are both your scalability strategy and your most likely DX failure source.** OFARM’s Pack Safety Policy explicitly calls out non-reproducible outcomes and impossible debugging as existential risks if pack compatibility isn’t deterministic. That is accurate. The transfer-pattern to adopt is “conformance classes + published tests”, as in OGC API standards, and “deprecation/compatibility discipline”, as in Kubernetes. (OFARM Pack Safety and Compatibility Policy v0.2, §10; OFARM conformance seed set v0.1.)

7) **Authority UX must look like a policy engine, not a permissions spreadsheet.** OFARM’s action-based authorisation and default deny is the correct core (and it already encodes stricter defaults for non-human / AI-assisted flows). To be usable, every deny needs an explainable decision trace, like mature authorisation systems and policy engines emphasise.

8) **Schema ergonomics are currently underpowered by missing “inline semantics” and “golden examples”.** JSON Schema is a good substrate, but schemas without descriptions/examples force humans and agents to reverse-engineer intent. The best ecosystems embed docs + examples into the contract surface (OpenAPI, AIP-192 style doc discipline, GraphQL’s introspective schema).

9) **Trace is not observability garnish; it is governance UX.** OFARM already demands explainability for materialisation (basis, context snapshot, freshness state and why) and has explicit enforcement failure classes (reject vs retain as draft vs contested vs require more evidence). To make that usable at scale, align trace propagation with Trace Context / OpenTelemetry, and standardise trace objects as first-class artefacts. (OFARM Current-State Materialization RFC v0.1, §2 & §6; OFARM Platform Enforcement Architecture Memo v0.1, §4.)

10) **Measure DX like a system, not vibes.** The DevEx literature converges on three forces: feedback loops, cognitive load, and flow state. OFARM can operationalise this with platform-native DX metrics: time-to-first-valid-query, time-to-resolve-pack-conflict, time-to-explain-deny, “stale-state caught before publish”, etc. Pair this with API usability evaluation methods and observation-based documentation research (developers start by building a global mental model, then diverge into concept-first vs code-first strategies).

## Developer UX problem map for OFARM

The goal here is not to make OFARM *simple*. It’s to make it **predictable, explorable, and hard to misuse** while preserving the constitutional/runtime split, assertion/history-first truth, governed materialisation, and twin boundary.

**Assertion/history-first truth and promotion rules**
Why hard: developers must reason about *claims vs in-force truth*, review/promotion paths, evidence sufficiency, and supersession/corrections, not just “write record, read record”. (OFARM Constitution RC2.1, §11; OFARM Platform Enforcement Architecture Memo v0.1, §4.)
Bad DX looks like: developers treat “submitted” or “AI-interpreted” as “true”; inconsistent behaviour between deployments; unclear paths from draft → accepted consequence → current-state.
Good DX looks like: a single “truth lifecycle” mental model, exposed as tooling: **capture → validate → evidence check → review → commit outcome → consequence → materialise** with explicit status objects and hyperlinks to basis/trace. (OFARM Constitution RC2.1, §11; OFARM Platform Enforcement Architecture Memo v0.1, §4.)
Strong transferable practices: structured failure objects (Problem Details), explicit “multi-issue” validation objects (OperationOutcome), and stable machine identifiers for error reasons (AIP-193).
Recommended OFARM direction: implement a **Promotion & Enforcement Trace** object (schema + viewer) that explains “what happened and what is required next” for every non-success outcome (reject/draft/contested/evidence-required/pack-conflict-deferred), and make it first-class in SDKs and the CLI. (OFARM Platform Enforcement Architecture Memo v0.1, §4.)

**Governed current-state materialisation and freshness policy**
Why hard: “current state” is not authoritative truth; it is a governed answer derived from basis + context + time policy. Freshness is purpose-sensitive (advisory may tolerate staleness; compliance publishing cannot). (OFARM Current-State Materialization RFC v0.1, §2 & §6.)
Bad DX looks like: teams silently rely on stale materialisations for high-consequence outputs; or they recompute too aggressively and create operational instability. (OFARM implementation risk memo after spike v0.1, §2.4.)
Good DX looks like: every current-state read comes with a **freshness label (FRESH/STALE/INVALID) and a machine-readable reason**, plus the basis identifiers used to compute it. (OFARM Current-State Materialization RFC v0.1, §6.)
Strong transferable practices: Kubernetes explicitly warns that OpenAPI validation is incomplete and recommends server-side dry-run to run full validation/admission; OFARM can mirror that separation between “cheap check” and “authoritative check”.
Recommended OFARM direction: make “freshness and why” unavoidable in high-consequence APIs. For example: any request that produces a DocumentAssembly/SubmissionAssembly must either (a) require FRESH materialisation, or (b) require an explicit override artefact whose creation is traceable (mirroring OFARM’s “override must itself become traceable truth”). (OFARM Current-State Materialization RFC v0.1, §6; OFARM Pack Safety and Compatibility Policy v0.2, §11.)

**Compliance Twin vs Advisory Twin boundary**
Why hard: two “spaces” on one substrate means developers can easily blur the semantics (especially when under time pressure). (OFARM Constitution RC2.1, §12; OFARM Platform Enforcement Architecture Memo v0.1, §8.)
Bad DX looks like: advisory hypotheses are used as compliance facts; cross-farm intelligence leaks into on-farm compliance truth without governance.
Good DX looks like: APIs and SDK types make the twin explicit (e.g., separate namespaces/types; compile-time friction), and the UI/CLI shows “Advisory” in a way that is hard to ignore.
Strong transferable practices: OWASP’s LLM security work explicitly elevates risks from excessive autonomy; the twin boundary is an architectural mitigation if the surface makes it hard to bypass.
Recommended OFARM direction: treat the twin boundary as a **product invariant**: documentation, SDK types, and runtime enforcement must all communicate “what cannot cross, and how it can cross when governed.”

**Pack activation, precedence, and merge semantics**
Why hard: packs are modular law; conflict resolution must be deterministic and explainable, or the platform becomes non-reproducible. OFARM already demands deterministic failure behaviour and forbids “partial hidden activation”. (OFARM Pack Safety and Compatibility Policy v0.2, §10.)
Bad DX looks like: “it works on my farm” behaviour; surprising changes when packs update; merge conflicts that are inscrutable; weak downgrade/rollback stories.
Good DX looks like: pack tooling that behaves like a serious configuration ecosystem: deterministic planning, explicit conflict traces, and conformance tests.
Strong transferable practices:
- OGC API standards explicitly define conformance classes and discovery operations; this makes partial implementations legible and testable.
- Kubernetes deprecation rules and version tracks (alpha/beta/GA) enforce stability expectations and warn on deprecated usage.
Recommended OFARM direction: formalise “pack conformance classes” and publish a **Pack Compatibility Test Suite** that tool builders can run locally. Make pack activation produce a conflict/fix plan object: conflicting packs, touched surface, precedence relationship, declared merge path, and “what would be required to resolve it” (this is already mandated; the DX step is to ship it as a concrete schema + CLI renderer). (OFARM Pack Safety and Compatibility Policy v0.2, §10; OFARM Pack Merge Semantics RFC v0.1.)

**Authority model, delegation, revocation, and action classes**
Why hard: developers must think in action classes and scope inheritance modes, not informal roles. Default deny is correct but punishing without good “why denied” traces. (OFARM Authority Policy Model RFC v0.1, §2.)
Bad DX looks like: “403 with no explanation”; engineers hardcode workarounds; audit trails are unreadable; third parties cannot predict what’s allowed.
Good DX looks like: every deny includes a stable reason code, evaluated conditions, and what grant would be required (or whether it’s human-only by default).
Strong transferable practices:
- IAM-style evaluation logic makes default-deny and explicit-deny precedence unambiguous; this is the mental model to teach, not “roles”.
- Authorisation systems like Zanzibar emphasise consistency and causal ordering of permission changes—relevant to OFARM’s prospective revocation and governed history.
- Policy engines emphasise debugging workflows and tooling (breakpoints, REPLs, traces).
Recommended OFARM direction: ship an **Authorisation Decision Explanation** artefact (schema + viewer) that is as important as the allow/deny itself.

**Query model: QuerySpecification, SemanticPathAlias, QueryPlanIR**
Why hard: the query model is intentionally semantically native, archetype/template-aware, and “safe for AI mediation”, with alias governance that must fail rather than guess. (OFARM Query Architecture Note v0.1, §1 & §6; OFARM QuerySpecification Schema RFC v0.1.)
Bad DX looks like: developers treat aliases as “hidden alternate schemas”; aliases drift and queries continue to validate but change meaning; QueryPlanIR feels magical.
Good DX looks like: most users follow “golden path queries” with cookbook patterns, and advanced users can inspect alias resolution + plan IR deterministically.
Strong transferable practices:
- GraphQL demonstrates how a strongly typed, introspectable schema enables tooling and reduces the need for extensive documentation for *using* the API (while still requiring serious work to build it).
- openEHR’s AQL demonstrates why archetype/path-level semantic querying exists: portability across storage and systems depends on semantic markers and path addressing.
Recommended OFARM direction: publish a **Query Cookbook** with executable fixtures (the RFC already includes examples) and ship `explainQuery`: (1) alias resolution report, (2) generated QueryPlanIR, (3) expected freshness constraints, (4) authority constraints detected.

**Enforcement chain and failure classes**
Why hard: OFARM is governance-heavy by design; users need to understand “reject vs retain as draft vs contested vs require more evidence vs deferred due to pack conflict.” (OFARM Platform Enforcement Architecture Memo v0.1, §4.)
Bad DX looks like: “it failed” with no category; developers can’t tell if retrying is sensible; operators implement unsafe bypasses.
Good DX looks like: every gate has a consistent failure response form and a consistent “next action” suggestion, and tooling can summarise traces as a pipeline.
Strong transferable practices: structured errors with stable identifiers and pointers (RFC 9457; AIP-193).
Recommended OFARM direction: define a single **EnforcementOutcome** schema family used across query, pack activation, assertion submission, review/promotion, and output compilation.

**Compiled outputs taxonomy: PassportView vs DocumentAssembly**
Why hard: “passport” previously overloaded multiple output families; OFARM now clarifies passport as scope summary, and distinguishes dossier/submission/report/document assemblies with different governance and attestation semantics. (OFARM Compiled Output and Passport Taxonomy Note v0.1.)
Bad DX looks like: consumers integrate to “passport” and then break when outputs diverge; developers confuse what is attestable, frozen, or merely view-shaped.
Good DX looks like: output types are explicit in API and SDK (type tags), and each has a clear production contract (inputs required, freshness required, evidence required).
Strong transferable practices: capability self-description patterns (FHIR CapabilityStatement) for what document/interaction modes a server supports.
Recommended OFARM direction: treat output types as a public contract surface with versioned schemas and strict compatibility rules (see “alias stability governance” debt).

DX lens on bounded debt (human impact):
- **Lot edge-case maturity** is the biggest “real world” trap: if lot continuity rules are unclear, integrators will either oversplit or create false continuity, breaking trust. (OFARM implementation risk memo after spike v0.1, §2.1.)
- **Alias stability** and **template merge safety** are the biggest “silent drift” traps: things appear to work until audits fail. (OFARM implementation risk memo after spike v0.1, §2.2–§2.3.)
- **Trace object formalisation** and **freshness-policy deepening** are the biggest “debugging tax” multipliers. (OFARM Current-State Materialization RFC v0.1; OFARM implementation risk memo after spike v0.1, §2.4.)
- **Capability manifest ecosystem maturity** is the biggest blocker to tool builders and third-party SDKs. (OFARM post gap closure readiness gate memo v0.1, §2; OFARM implementation risk memo after spike v0.1, §2.5.)

## AI-agent UX problem map for OFARM

AI agents are not “fast humans”. They fail differently: they overgeneralise from partial patterns, hallucinate “close enough” API shapes, retry destructively, and optimise for completion rather than governance unless bounded. Your baseline already anticipates this (AI is part of runtime; AI outputs must enter enforcement; human-only governance by default). The point is to make the platform **machine-consumable without being machine-controllable**.

**Assertion/history-first truth and promotion rules**
Why hard for agents: the platform has multiple intermediate states (draft, contested, evidence-required) that look like “success” to a naïve agent unless the contract forces correct interpretation. (OFARM Platform Enforcement Architecture Memo v0.1, §4 & §8.)
Likely failure modes:
- treating “draft assertion recorded” as “in-force truth”;
- attempting to auto-promote;
- generating plausible-looking evidence links that don’t satisfy policy.
Strong practices: separate *tooling affordances* (proposal vs commit) and require explicit promotion tokens / human approval for high-governance actions (mirrors MCP’s control hierarchy: tools are model-controlled, but the protocol separates user-controlled vs application-controlled primitives).
Recommended OFARM direction: every “mutating” endpoint should support a **preflight** mode that returns an EnforcementOutcome and “required approvals/evidence” without mutating compliance truth.

**Governed current-state and freshness**
Why hard for agents: “freshness is purpose-sensitive” requires contextual reasoning; agents will default to “use the latest value” unless staleness is encoded. (OFARM Current-State Materialization RFC v0.1, §6.)
Failure modes:
- using STALE state to generate compliance outputs;
- ignoring INVALID and retrying blindly;
- oscillating recomputation loops because triggers are misunderstood.
Strong practices: make staleness a *typed constraint*, not a warning string (e.g., response includes `freshness: STALE` with a machine-readable reason and a “must recompute for useClass=COMPLIANCE_PUBLISH”).
Recommended OFARM direction: encode use-class constraints in machine-readable contracts and enforce them server-side; return structured remediation.

**Twin model boundary**
Why hard for agents: agents naturally mix sources; without strong boundaries, advisory outputs will contaminate compliance state.
Failure modes: “helpful” agent writes advisory interpretation back into compliance surfaces; cross-scope inference leaks.
Strong practices: hard constraints + tool separation; OWASP explicitly flags “excessive agency” as a major risk category for LLM applications.
Recommended OFARM direction: custody model in tooling: advisory tooling can *propose* compliance actions as a package, but cannot execute them without explicit governed bridging.

**Pack activation and merges**
Why hard for agents: pack compatibility is a graph of constraints; agents may attempt to “fix” conflicts by ad-hoc edits that violate precedence law. (OFARM Pack Safety and Compatibility Policy v0.2, §10–§11.)
Failure modes:
- partial activation (if the platform ever allows it, agents will exploit it unintentionally);
- “resolve conflict” by deleting constraints;
- choosing an unsafe merge when the correct action is HARD_FAIL.
Strong practices: deterministic, proof-carrying merge outputs—if the system “cannot prove semantic compatibility”, it should hard fail (this is already in pack merge semantics). (OFARM Pack Merge Semantics RFC v0.1, §5.1.)
Recommended OFARM direction: merge resolution should produce a **PackMergeResolutionTrace** (the spike notes already anticipate it) with explicit “why safe” or “why hard fail”, so an agent can’t rationalise around it. (OFARM reference implementation spike design notes v0.1, §4.3.)

**Authority model**
Why hard for agents: agents need tight action-scoped permissions and predictable denies; “role” metaphors are too fuzzy. (OFARM Authority Policy Model RFC v0.1, §2.)
Failure modes: retry storms on deny; attempting alternative endpoints (hallucinated capability); insisting on doing human-only actions.
Strong practices: action-based permits plus decision explanations; policy engines emphasise debugging facilities and tools.
Recommended OFARM direction: “deny with remediation”: return a stable reason code and whether the action is human-only by default, matching the Authority Action Matrix concept (“AI-assisted default” is an explicit attribute today). (OFARM Authority Action Matrix v0.1.)

**Query model and aliases**
Why hard for agents: they will overfit to examples and reuse stale aliases, or invent plausible aliases. OFARM explicitly says alias resolution should fail clearly rather than guess. (OFARM Query Architecture Note v0.1, §6.)
Failure modes: hallucinated alias names; using a deprecated alias silently; confusing `targetTwin` semantics; generating queries that validate but are semantically nonsensical.
Strong practices: introspection and schema-driven tooling; GraphQL demonstrates that introspection is a “platform for tool-building” and that strong typing enables pre-execution validation.
Recommended OFARM direction: provide an **Alias Registry endpoint** with machine-readable status (active/deprecated/removed), plus a “suggested replacement alias” field; treat alias deprecation like an API deprecation policy (warn early, provide timelines, provide migration docs).

**Enforcement chain and failure classes**
Why hard for agents: they need to choose next actions correctly; “retain as draft” vs “reject” implies different next steps. (OFARM Platform Enforcement Architecture Memo v0.1, §4.)
Failure modes: looping retries, or escalating privilege attempts; misclassifying a contested outcome as success.
Strong practices: explicit outcome categories; structured errors with “instance” identifiers for trace correlation.
Recommended OFARM direction: agents should receive a standard `outcome.kind` plus `nextActions[]` suggestions that are safe and bounded (e.g., “request human review”, “attach evidence”, “recompute materialisation”).

**Outputs taxonomy**
Why hard for agents: agents generate artefacts; if they don’t understand which outputs are attestable or filing-grade, they will produce the wrong thing. (OFARM Compiled Output and Passport Taxonomy Note v0.1.)
Failure modes: treating a PassportView as a SubmissionAssembly; skipping required evidence/attestation steps.
Strong practices: capability self-description and conformance declarations; FHIR-style capability statements and OperationOutcome-style errors for operation-specific constraints.
Recommended OFARM direction: expose output compilation as “plan then render then approve then attest” with machine-readable required steps.

DX lens on bounded debt (agent impact):
- **Capability honesty** (manifest valid JSON but misleading) is a top agent failure source because agents trust machine-readable declarations. (OFARM implementation risk memo after spike v0.1, §2.5.)
- **Trace-object schema formalisation** is mandatory for safe agent operations; without it, agents can’t self-correct and will retry blindly.
- **Alias stability** is more dangerous for agents than humans because agents will reuse patterns at scale. (OFARM implementation risk memo after spike v0.1, §2.2.)
- **Freshness-policy deepening** is a key “agent safety” mechanism: purpose-sensitive freshness must be encoded, not implied. (OFARM Current-State Materialization RFC v0.1, §6.)

## Best-practice synthesis by topic

**Documentation information architecture**
Use the Diátaxis model explicitly: tutorials (learning), how-to guides (task completion), reference (lookup), and explanation (conceptual understanding). The key reason is that developers switch modes; good docs respect that instead of mixing them.
Empirical documentation research indicates developers first try to build a global understanding of an API’s purpose/features, then diverge into concept-oriented vs code-oriented learning strategies—docs must satisfy both.
OFARM-specific synthesis:
- Your “explanations” must carry the constitutional/runtime split, twin boundary, and truth/materialisation model.
- Your “reference” must be the QuerySpecification/QueryPlanIR schemas, authority action classes, pack surfaces, and output taxonomies, with stable examples.
- Your “how-to” must be persona-specific (integrator vs pack author vs tooling builder vs conformance author).
- Your “tutorials” must be “golden path” vertical slices (see roadmap).

**API and schema ergonomics for complex platforms**
Contract-first is non-negotiable when complexity is inherent. OpenAPI is explicitly designed so both humans and computers can “discover and understand capabilities” and drive documentation/codegen/testing.
JSON Schema 2020-12 provides a modern vocabulary model plus defined output formats; use those output formats intentionally for validator UX (basic/detailed/verbose).
OFARM-specific synthesis:
- Add **descriptions and examples** throughout OFARM schemas (QuerySpecification, CapabilityManifest, traces).
- Publish an OpenAPI surface for runtime endpoints, and ensure schema refs match the canonical JSON schemas to avoid drift.
- Adopt a “linted contract” discipline (AIP-192 is a good template for “everything must be documented” rules, even if OFARM isn’t protobuf-based).

**Capability self-description and negotiation**
Kubernetes publishes both discovery summaries and OpenAPI schemas, and clients cache them for tooling.
FHIR requires servers to provide capability statements and uses them as the canonical discovery mechanism; it also demonstrates how errors become computable objects (OperationOutcome).
OFARM-specific synthesis:
- Treat OFARM Capability Manifest as both **human-readable posture** and **machine-negotiable contract**.
- Provide authority-scoped capability views (what this credential can actually do) to reduce misuse, like capability statements may vary per user context.
- Add a “capability honesty” validation layer: manifest must be checked against the deployed artefact graph to reduce lying-by-omission risk. (OFARM implementation risk memo after spike v0.1, §2.5.)

**SDK/CLI/tooling ergonomics**
Terraform’s ecosystem shows the value of explicit versioned protocols and code generation from a shared intermediate representation—it reduces divergence across providers.
OFARM-specific synthesis:
- Generate typed SDKs from OFARM JSON Schema and OpenAPI (for integrators and tool builders).
- Provide a CLI that can: validate artefacts; run conformance suites; render traces; diff capability manifests; and “plan” pack activation (show conflicts without applying).
- Ship a local sandbox (containerised) that includes fixtures and golden path examples.

**Validation, errors, and denial messaging**
RFC 9457 defines a standard machine-readable error envelope and explicitly warns about leaking sensitive data while still supporting remediation.
AIP-193 gives a concrete pattern for stable machine identifiers and metadata so clients don’t parse strings.
FHIR OperationOutcome provides multi-issue reporting with expression pointers, enabling UI/tooling alignment.
OFARM-specific synthesis:
- Standardise: `error.type` (URI), `error.code` (stable reason), `error.instance` (trace id / occurrence id), `error.pointers[]` (JSON Pointer / semantic path / alias ref), and `remediation[]`.
- For authorisation denies: include evaluated action class, scope inheritance mode used, and whether it is human-only by default. (OFARM Authority Policy Model RFC v0.1; OFARM Authority Action Matrix v0.1.)

**Trace, debugging, and explainability UX**
Trace Context standardises propagation of request context for distributed tracing.
OpenTelemetry formalises SpanContext and aligns to Trace Context.
OFARM-specific synthesis:
- Define “governance traces” as first-class artefacts: PromotionTrace, PackMergeResolutionTrace, AuthorisationDecisionTrace, MaterializationBasisTrace, QueryExplainTrace.
- Make every “instance” link resolvable via the platform (with appropriate authorisation), so a developer can pivot from an error to the exact enforcement path.

**Conformance UX**
OGC API standards explicitly define conformance classes; this makes partial implementations legitimate and testable rather than “mystery incomplete”.
Kubernetes enforces strict constraints on API evolution and publishes migration/deprecation guidance.
OFARM-specific synthesis:
- Publish OFARM conformance classes for: packs, authority decisions, query planning, materialisation freshness semantics, outputs taxonomy.
- Scale your seed set into an executable test suite (you already have a seed set targeting the highest-risk seams). (OFARM conformance seed set v0.1.)
- Treat conformance as developer tooling: `ofarm test`, `ofarm explain`, `ofarm validate`, not a compliance afterthought.

**AI-agent-facing interfaces and constraints**
MCP formalises capability negotiation and separates primitives by control (user-controlled prompts, application-controlled resources, model-controlled tools). This is a useful mental model for OFARM’s “AI is in runtime but bounded”.
The Top 10 for LLM Applications 2025 highlights prompt injection and excessive agency as primary threat categories; OFARM’s default-deny + human-only high-governance posture aligns with that, but must be enforced via contracts and tooling.
OFARM-specific synthesis:
- Provide an “Agent Use Contract” that defines: allowed toolset, max autonomy level per action class, required approvals, and required trace emission.
- Ensure every tool/endpoint is discoverable via Capability Manifest and OpenAPI, so an agent can’t plausibly hallucinate “maybe it exists”.

**Safe default abstractions**
The right abstraction strategy is not “hide complexity”; it’s “default to safe paths and make unsafe paths expensive.”
OFARM-specific synthesis:
- “Advisory by default” for AI-mediated outputs; explicit bridge for compliance truth. (OFARM Platform Enforcement Architecture Memo v0.1, §8.)
- Provide opinionated starter packs and profiles that define safe default behaviour, while making overrides explicit and traceable. (OFARM Pack Safety and Compatibility Policy v0.2, §11.)

**Sandbox, starter kit, and examples**
The platform already validated a spike harness with deterministic results on critical seams; that is the kernel of a developer sandbox and conformance runner. (OFARM reference spike harness run results v0.1.json; PASS_WITH_LIMITATIONS.)
OFARM-specific synthesis:
- One “hello world” that ends in a PassportView, not a sprawling demo.
- One “hard path” demo that forces: pack conflict → explanation → override artefact → success, because this is where developer trust is won.

## OFARM-specific recommendations

**Adopt now**
- **Ship a single cross-cutting error envelope** (Problem Details-compatible) and require it in every endpoint and every CLI subcommand output. Use stable reason codes and pointer fields; stop relying on prose-only errors.
- **Make “explain” endpoints mandatory** for the core seams: `explainAuthz`, `explainPackActivation`, `explainQuery`, `explainMaterialization`. If an outcome is governance-sensitive, it must be explainable (this is already a constitutional stance; enforce it as UX). (OFARM Current-State Materialization RFC v0.1, §2.3; OFARM Platform Enforcement Architecture Memo v0.1, §4.)
- **Adopt a doc architecture explicitly shaped by Diátaxis**, and publish persona entry points.
- **Turn the conformance seed set + harness into a developer tool**: `ofarm conformance test` with readable diffs and trace links. (OFARM conformance seed set v0.1; OFARM reference spike harness run results v0.1.json.)

**Prototype next**
- **Capability Manifest as live discovery surface**: serve it from the runtime, support scoped views (per credential), and provide a diff tool for capability negotiation. Use the “discovery summary + full schema” duality pattern seen in Kubernetes (Discovery + OpenAPI).
- **PackMergeResolutionTrace and Override artefact workflows**: make pack conflicts produce a fix plan object and support a governed override artefact generator instead of “operator memory”. (OFARM Pack Safety and Compatibility Policy v0.2, §10–§11.)
- **Alias governance tooling**: create an Alias Registry with status, deprecation warnings, and automatic detection of “semantic drift risk” in queries. (OFARM Query Architecture Note v0.1, §6; OFARM implementation risk memo after spike v0.1, §2.2.)
- **Trace object schema family aligned to Trace Context/OpenTelemetry** so traces can flow through external tooling without OFARM becoming a tracing snowflake.

**Avoid**
- **Do not standardise a public textual query language too early.** OFARM’s stance (“internal model first, public syntax later”) is correct; freezing syntax prematurely will lock in mistakes and increase long-term DX debt. (OFARM QuerySpecification Schema RFC v0.1, §2.1.)
- **Do not permit partial hidden pack activation** under any circumstances; it will become the “works until audit” disaster mode. (OFARM Pack Safety and Compatibility Policy v0.2, §10.)
- **Do not let schema validation become a false guarantee.** Publish explicit statements of what JSON Schema validates vs what runtime enforcement validates (mirroring Kubernetes’ warning that OpenAPI validation is incomplete).

**High-risk if ignored**
- **Trace-object schema formalisation**: without stable trace schemas and “instance” correlation, both human and agent workflows degrade into superstition and retries.
- **Capability honesty**: if Capability Manifests can be “valid but misleading”, external tool builders (and agents) will fail unpredictably and lose trust. (OFARM implementation risk memo after spike v0.1, §2.5.)
- **Freshness policy deepening**: if STALE is operationally tolerated in compliance-grade flows, OFARM will fail as a trustworthy standard. (OFARM Current-State Materialization RFC v0.1, §6; OFARM implementation risk memo after spike v0.1, §2.4.)
- **Template merge validator maturity**: if “declared safe merge” is under-specified, you will get implementation divergence across deployments—fatal for a standard. (OFARM implementation risk memo after spike v0.1, §2.3.)

## Suggested artifact improvements

What follows are concrete artefacts that directly reduce developer and agent failure modes.

- **Developer portal structure (Diátaxis + personas)**:
  - Tutorials: “First PassportView from seed fixtures”; “First pack activation and conflict”.
  - How-to: “Author an ObservationEvent”, “Attach evidence”, “Request review”, “Generate QueryPlanIR and explain it”, “Run conformance locally”.
  - Reference: schemas (QuerySpecification, QueryPlanIR, Capability Manifest, enforcement traces), error catalogue, action-class catalogue, pack surface catalogue.
  - Explanation: Constitution vs Platform law, twin boundary, truth lifecycle, freshness semantics.

- **Error catalogue and problem-type registry**: one canonical list of error “types” and stable reason codes, with remediation guidance and security guidance on what must not be leaked.

- **Trace object schema family**:
  - `AuthorisationDecisionTrace` (inputs, evaluated grants, inheritance mode, result).
  - `PackActivationTrace` + `PackMergeResolutionTrace`.
  - `MaterializationBasisTrace`.
  - `QueryExplainTrace` (alias resolution, plan IR, executor chain).
  Align the trace identifiers with Trace Context and expose an “instance retrieval” endpoint.

- **Capability Manifest “live spec” docs**: formalise what each manifest field means operationally, and add a validator that checks manifest consistency against deployed artefact state (mitigates “capability honesty” risk). (OFARM Capability Manifest RFC v0.1; OFARM implementation risk memo after spike v0.1, §2.5.)

- **Query cookbook + executable fixtures**: expand the included fixtures (field passport current-state, lot lineage, etc.) into a versioned cookbook where each recipe includes: QuerySpecification JSON, generated QueryPlanIR, and expected enforcement outcomes. (OFARM QuerySpecification Schema RFC v0.1, §2.2; OFARM Query Architecture Note v0.1.)

- **Pack authoring guide with merge semantics table**: document the safe merge modes (e.g., HARD_FAIL, STRONGEST_REQUIREMENT) and provide a CLI tool that simulates merge outcomes and prints traces. (OFARM Pack Merge Semantics RFC v0.1.)

- **AI-agent use contracts** (separate from human docs):
  - Machine-readable “tool manifests” (OpenAPI + JSON Schema + examples).
  - Explicit “human-only by default” action class flags surfaced via runtime discovery. (OFARM Authority Action Matrix v0.1; OFARM Authority Policy Model RFC v0.1.)
  - A minimal agent workflow: propose → preflight → request approval → execute → emit trace.

- **Conformance fixtures and harness packaging**: ship the harness as a distributable artefact with a stable CLI interface; publish conformance classes and a public test suite plan (like OGC’s conformance class approach).

## Prioritized roadmap

**Immediate**
- Standardise the error envelope and require it everywhere (platform + tooling).
- Convert the spike harness into a supported developer tool (installable CLI) and publish “seed conformance” as the canonical DX entry point. (OFARM conformance seed set v0.1; OFARM reference spike harness run results v0.1.json.)
- Publish the first “golden path” tutorial that exercises: ingest → assertion → enforcement outcome → current-state materialisation → PassportView output, with full traces.

**Near-term**
- Capability Manifest becomes runtime-served discovery, with per-credential scoping and diff tooling; publish OpenAPI for runtime endpoints and ensure it is consistent with JSON schema contracts.
- Introduce trace schema family + trace viewer, aligned with Trace Context.
- Implement “plan vs execute” surfaces for the major seams: query, pack activation, compilation, and promotion; add server-side “dry-run/preflight” endpoints.

**Later**
- Expand conformance to “at scale” scenarios: larger pack graphs, richer lot edge cases, multi-party authority boundaries, and long-lived alias deprecation sequences. (OFARM post gap closure readiness gate memo v0.1, §2; OFARM implementation risk memo after spike v0.1, §2.)
- Formalise and harden alias stability governance with explicit deprecation policy and tooling enforcement (warnings, metrics, migration guides), mirroring mature API evolution practices.
- Mature the “agent-focused contract surface”: machine-readable affordances, strict safety defaults, and “bounded autonomy” patterns that are auditable and testable against OWASP-like risk categories.

## Annotated bibliography

**Documentation and DX measurement**
- Diátaxis foundations (decisive for doc IA; four doc modes mapped to user needs).
- Empirical evidence that developers first form a global understanding, then diverge into concept-first vs code-first learning strategies (highly relevant to OFARM onboarding).
- DevEx framework (feedback loops, cognitive load, flow state) — useful for defining measurable DX targets rather than vague “make docs better”.
- Mapping study of API usability evaluation methods (useful for designing OFARM-specific DX evaluation).

**Error models and validation UX**
- RFC 9457 Problem Details (baseline standard for machine-readable HTTP errors; includes security considerations).
- AIP-193 Errors (decisive pattern for stable machine-readable error identifiers + metadata without parsing messages).
- FHIR OperationOutcome (domain-grade multi-issue error object with expression pointers; useful inspiration for OFARM validator feedback).

**Contract-first APIs, schemas, and introspection**
- OpenAPI 3.1 (core standard for machine- and human-consumable API definitions; supports docgen/codegen/testing).
- JSON Schema 2020-12 (OFARM already uses it; leverage its output formats and vocabulary discipline intentionally).
- GraphQL spec (decisive for “introspection as tooling platform” and strong typing as pre-execution validation).
- openEHR AQL spec (good analogue for archetype/path-level querying portability in a template/archetype-governed domain).

**Discovery, conformance, and ecosystem scalability**
- Kubernetes API publication via Discovery + OpenAPI; includes warning about schema incompleteness and recommendation of server-side dry-run.
- Kubernetes deprecation policy (clear rules for evolution and compatibility).
- OGC API Features core spec (decisive for conformance classes + discovery operations as standard-grade interoperability scaffolding).
- FHIR CapabilityStatement (useful analogue for capability self-description as a mandatory part of interoperability).

**Policy, authority, and explainability tooling**
- “Zanzibar” paper (important precedent for globally consistent authorisation with causal ordering; relevant to governed history and prospective changes).
- IAM evaluation logic (clear articulation of default-deny and explicit-deny precedence; relevant mental model for OFARM action-based authorisation UX).
- OPA debugging and policy language docs (useful for how policy ecosystems support REPL/debug adapters/strict checking).
- Cedar (authorisation language designed for analyzable policy; relevant as a “policy UX” comparator).

**AI-agent interoperability and safety**
- MCP specification and control hierarchy (decisive for capability negotiation patterns and separating user/app/model control).
- Top 10 for LLM Applications 2025 (useful threat framing; supports why OFARM must enforce strict autonomy boundaries and traceability).

**Tracing and audit correlation**
- Trace Context (standard for propagation headers; relevant for cross-system trace correlation).
- OpenTelemetry tracing API notes alignment with Trace Context and defines SpanContext semantics (useful for implementing OFARM trace objects in a tool-compatible way).

**OFARM internal baseline sources consulted**
OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md; OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md; OFARM_Alignment_Register_v0_13.md; OFARM_final_hostile_review_after_gap_closure_v0_1.md; OFARM_post_gap_closure_readiness_gate_memo_v0_1.md; OFARM_Query_Architecture_Note_v0_1.md; OFARM_QuerySpecification_Schema_RFC_v0_1.md; OFARM_QuerySpecification_schema_v0_1.json; OFARM_QueryPlanIR_schema_v0_1.json; OFARM_Capability_Manifest_RFC_v0_1.md; OFARM_Capability_Manifest_schema_v0_1.json; OFARM_Pack_Safety_and_Compatibility_Policy_v0_2.md; OFARM_Pack_Merge_Semantics_RFC_v0_1.md; OFARM_Authority_Policy_Model_RFC_v0_1.md; OFARM_Authority_Action_Matrix_v0_1.md; OFARM_Current_State_Materialization_RFC_v0_1.md; OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md; OFARM_Platform_Enforcement_Architecture_Memo_v0_1.md; OFARM_reference_implementation_spike_design_notes_v0_1.md; OFARM_conformance_seed_set_v0_1.md; OFARM_implementation_risk_memo_after_spike_v0_1.md; OFARM_reference_spike_harness_run_results_v0_1.json.
