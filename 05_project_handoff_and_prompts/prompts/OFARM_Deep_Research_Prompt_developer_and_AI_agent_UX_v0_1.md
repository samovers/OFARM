# Deep Research Prompt — OFARM developer experience and AI-agent experience

You are doing **Deep Research** for **OFARM**, a semantically native crop-farming operating standard and platform architecture.

## Mission

OFARM now appears powerful but also complex.

One of the most important conditions for OFARM to become a serious standard-grade platform is that it must become **easy and trustworthy to use for developers** and also **easy and safe for AI coding agents / AI software agents** to work with.

Your task is to research:
- the best papers
- best practices
- technical design patterns
- strong examples from other ecosystems
- usability methods
- DX (developer experience) methods
- machine-consumable platform design methods

that can help OFARM achieve the **best possible user experience for developers and AI coding agents using the platform**.

This is not a general product UX task.
This is specifically about:
- **developer experience**
- **platform ergonomics**
- **tooling ergonomics**
- **schema/contract ergonomics**
- **integration ergonomics**
- **AI-agent consumability**
- **safe machine-use of a governance-heavy platform**

Do **not** focus on:
- politics
- lobbying
- procurement
- commercial adoption strategy
- pricing or business model

---

## Read these project files first

You must read these before researching:

### Core active baseline
- `OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `OFARM_Alignment_Register_v0_13.md`

### Current top-level judgment
- `OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

### DX-relevant companion artifacts and RFCs
- `OFARM_Query_Architecture_Note_v0_1.md`
- `OFARM_QuerySpecification_Schema_RFC_v0_1.md`
- `OFARM_QuerySpecification_schema_v0_1.json`
- `OFARM_QueryPlanIR_schema_v0_1.json`
- `OFARM_Capability_Manifest_RFC_v0_1.md`
- `OFARM_Capability_Manifest_schema_v0_1.json`
- `OFARM_Pack_Safety_and_Compatibility_Policy_v0_2.md`
- `OFARM_Pack_Merge_Semantics_RFC_v0_1.md`
- `OFARM_Authority_Policy_Model_RFC_v0_1.md`
- `OFARM_Authority_Action_Matrix_v0_1.md`
- `OFARM_Current_State_Materialization_RFC_v0_1.md`
- `OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
- `OFARM_Platform_Enforcement_Architecture_Memo_v0_1.md`

### Implementation-reality and conformance artifacts
- `OFARM_reference_implementation_spike_design_notes_v0_1.md`
- `OFARM_conformance_seed_set_v0_1.md`
- `OFARM_implementation_risk_memo_after_spike_v0_1.md`
- `OFARM_reference_spike_harness_run_results_v0_1.json`

You are not allowed to ignore the baseline and answer as if OFARM were a blank slate.

---

## OFARM baseline assumptions you must preserve

Assume all of the following are already decided:

- OFARM has a **model/runtime split**
  - Constitution = model law
  - Platform = runtime law

- Canonical truth is **assertion/history-first**
- Current state is a **governed materialization**
- There is **one semantic substrate**
- There are two logical twins:
  - Compliance Twin
  - Advisory Twin

- OFARM has:
  - explicit event grammar
  - explicit commit classes
  - explicit pack law
  - explicit authority / delegation / revocation law
  - internal query model with QuerySpecification and QueryPlanIR
  - PassportView / DocumentAssembly output taxonomy
  - enforcement-chain runtime concept
  - Capability Manifest as runtime self-description

- OFARM is currently judged:
  - **implementation-directed with bounded debt**
  - **not yet externally standard-ready**

Do not suggest flattening OFARM into a simple CRUD model just to improve DX.
The challenge is:
**how to preserve the architecture while making it much easier to use well.**

---

## What “developer and AI-agent UX” means in this research

You must explicitly cover **both**:

### A. Human developer experience
Examples:
- platform consumers
- integrators
- internal platform developers
- extension/profile/pack authors
- tool builders
- API and SDK users
- conformance/test authors

### B. AI coding agent / AI software agent experience
Examples:
- Codex-like implementation agents
- agentic integration assistants
- AI-assisted query authors
- AI-assisted pack/profile authors
- AI-assisted tooling using machine-readable contracts

You must treat these as **related but different UX problems**.

---

## Main research questions

Research these questions deeply.

### 1. How do you make a powerful semantic/governance-heavy platform easy for developers to understand?
Look for best practices on:
- information architecture for platform docs
- layered onboarding
- concept minimization
- progressive disclosure
- reference + tutorial + conceptual docs balance
- examples, recipes, and “golden paths”
- reducing conceptual overload without hiding necessary rigor

### 2. How do you design APIs, schemas, and contracts for strong DX in complex platforms?
Look for research and strong practice on:
- API ergonomics
- schema ergonomics
- contract-first design
- discoverability
- introspection
- naming
- consistency
- example-driven design
- typed SDKs / generated clients / codegen
- error reporting
- capability negotiation
- versioning and deprecation UX

### 3. How do you make a platform easy for AI agents to use safely?
Research best practices for:
- machine-readable capability descriptions
- machine-readable tools/resources
- self-describing contracts
- action safety boundaries
- preventing unsafe autonomy
- traceability for AI-triggered actions
- design patterns that reduce hallucinated usage
- how to structure docs/specs for agent consumption
- how to expose platform affordances in ways that are easy for agents to plan with

### 4. What makes a platform “feel usable” to developers when the domain model is inherently complex?
Research:
- good vs bad examples
- comparable ecosystems
- successful contract-heavy / schema-heavy / compliance-heavy platforms
- SDK + CLI + test harness + sandbox patterns
- local developer environments
- debugging and trace visualization
- conformance workflows that developers will actually use

### 5. How should OFARM present and package its complexity?
Research:
- concept bundling
- profile-based onboarding
- opinionated starter packs
- starter templates and reference apps
- path-specific docs for different personas
- reducing the chance of misuse of advanced concepts
- how much should be “defaulted” vs “configured”

### 6. How should OFARM expose its hardest concepts to developers?
Specifically:
- assertion/history-first truth
- current-state freshness
- twin model
- pack activation and merge
- authority action model
- query model
- PassportView vs DocumentAssembly
- evidence and promotion rules

The research should answer:
- what should be first-class in DX
- what should be hidden behind safer abstractions
- what should be visible but guided
- what should be advanced-only

### 7. How do you make conformance, debugging, and failure states usable?
Research best practices for:
- validation feedback
- trace explainability
- debugging tools
- contract mismatch feedback
- merge conflict explanation
- authorization denial explanation
- freshness/staleness explanation
- test fixture experience
- developer sandbox design

### 8. Which external ecosystems are best analogues for OFARM DX?
Consider, where relevant:
- Stripe
- Terraform / provider ecosystems
- Kubernetes CRDs / operators
- GraphQL ecosystems
- FHIR / openEHR ecosystems
- OGC / geospatial APIs
- event-driven platforms
- policy engines
- typed SDK ecosystems
- model-driven engineering environments
- MCP-like tool/resource descriptions for agent use

Do not just name-drop them. Explain which patterns transfer and which do not.

---

## Special focus areas

You must explicitly analyze OFARM’s current **bounded debt** through a DX lens:

- lot edge-case maturity
- alias-stability governance
- template-merge validator maturity
- trace-object schema formalization
- freshness-policy deepening
- capability-manifest ecosystem/tooling maturity
- deeper conformance at scale

Ask:
- which of these are most damaging to developer UX?
- which of these are most damaging to AI-agent UX?
- how should OFARM mitigate them in platform design and documentation?

---

## Research method requirements

- Use **primary sources first**:
  - formal standards
  - official documentation
  - peer-reviewed papers
  - strong technical reports
  - engineering writeups from credible organizations
- Use recent sources for rapidly changing AI-agent/tooling topics.
- Distinguish:
  - strongly evidence-backed practices
  - good but mostly practitioner-driven practices
  - speculative or weakly supported ideas
- When multiple approaches compete, compare them explicitly.

---

## Required output

Produce a report with these sections:

### 1. Executive summary
- the 10 most important findings for OFARM developer UX and AI-agent UX

### 2. Developer UX problem map for OFARM
For each major OFARM complexity area:
- why it is hard for developers
- what bad DX would look like
- what good DX would look like
- strongest external practices
- recommended OFARM direction

### 3. AI-agent UX problem map for OFARM
For each major OFARM complexity area:
- why it is hard for AI coding agents / software agents
- likely failure modes
- strongest practices for machine-consumable design
- recommended OFARM direction

### 4. Best-practice synthesis by topic
At minimum:
- docs/information architecture
- API/schema ergonomics
- capability self-description
- SDK/CLI/tooling design
- validation/error messaging
- trace/debug UX
- conformance UX
- AI-agent-facing interfaces and constraints
- safe default abstractions
- sandbox / starter kit / example strategy

### 5. OFARM-specific recommendations
Give concrete recommendations under headings like:
- adopt now
- prototype next
- avoid
- high-risk if ignored

### 6. Suggested artifact improvements
Recommend which OFARM artifacts should probably be added or strengthened, such as:
- docs structure
- developer portal structure
- API / SDK conventions
- trace object schemas
- starter examples
- manifest/discovery docs
- query cookbook
- pack authoring guides
- AI-agent use contracts
- conformance fixtures / sandboxes / harnesses

### 7. Prioritized roadmap
A realistic staged DX roadmap for OFARM:
- immediate
- near-term
- later

### 8. Annotated bibliography
Group by topic and mark the most decisive sources.

---

## Output style

- Be blunt.
- Use citations for all load-bearing claims.
- Do not give generic “improve docs” advice.
- Tie everything back to OFARM specifically.
- Explicitly distinguish:
  - what helps human developers
  - what helps AI agents
  - what helps both
- If OFARM is currently too complex in a specific place, say so and explain how to simplify the *experience* without flattening the architecture.
