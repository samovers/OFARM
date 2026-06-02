# OFARM 2 migration inventory and recommendation v0.6

Status: historical inventory through the v0.6 migration seed
Current package entrypoint: `README.md`
Current post-v0.6 change trail: `CURRENT_PACKAGE_CHANGELOG.md`

Date: 2026-04-08

## Executive judgment

**Yes — OFARM 2 is ripe to move into its own project.**

But the right move is **not** “copy everything”.
It is a **curated migration** with four buckets:

1. **migrate as active authority**
2. **migrate as active support**
3. **migrate as reference-only legacy source**
4. **do not migrate**

The new project should start from the **RC2.1 baseline**, not from old `fa_rm` / `farm_rm` naming or old repo structure.

## What I used

I used:
- this thread’s outputs
- the current project-visible OFARM 2 baseline and RFC artifacts in `/mnt/data`
- the visible legacy repo packages `fa_rm-1.0.26.zip` and `fa_rm-1.0.25.zip`
- the project-visible legacy docs/resources surfaced through those packages

I did **not** use invisible/raw transcripts from other chats outside what is reflected in the project-visible artifacts.

## Recommended migration buckets

### A. Migrate as active authority
These should become the new project’s canonical starting point:

- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

This is the real OFARM 2 starting set.

### B. Migrate as active support
These should move too, because they materially help continuation:

- `04_implementation_and_conformance/`
- `05_project_handoff_and_prompts/`

These are not constitutional authority, but they are useful continuation assets.

### C. Migrate as curated legacy reference only
Everything under:

- `legacy_reference/fa_rm_v1/`

should be treated as:
- **read-only**
- **reference-only**
- **non-authoritative unless explicitly promoted later**

These files are useful because they preserve:
- old domain thinking
- old runtime seams
- old product direction
- old implementation patterns
- old API and ontology lineage

But they must not quietly override RC2.1.

### D. Do not migrate
Do **not** carry the following into the new project as normal working material:

- the whole old repo as-is
- old `fa_rm` / `farm_rm` package roots
- intermediate RC1 drafts
- intermediate working-plan versions
- phase-by-phase repair notes
- superseded patch docs
- duplicate zip bundles
- `fa_rm-1.0.25.zip` unless you want archaeology or diffs
- broad generated historical clutter that is already superseded by RC2.1 + accepted RFCs

If you keep any of that, keep it outside the new project as cold archive only.

## Recommended new project structure

Suggested top-level shape:

- `baseline/`
- `companion_artifacts/`
- `rfcs/accepted/`
- `machine_contracts/`
- `implementation_and_conformance/`
- `prompts_and_handoff/`
- `legacy_reference/fa_rm_v1/`
- `archive/` (optional, but ideally outside the new project)

## Why the curated legacy subset is the right one

### Legacy context/onboarding
Move these because they explain the old repo and old semantic/runtime worldview quickly:
- old project context
- AI onboarding pack
- repo map
- semantic/runtime/compliance/status/open-questions summaries

### Legacy research
Move these because they still help OFARM 2 thinking:
- everyday farm use-cases gap analysis
- agronomy archetype authority review
- selected farman-lite content-gap materials

### Legacy product/implementation packets
Move these because they still contain the best old thinking about:
- field passport
- voice session / conversational capture
- AI capture assist / intake
- operation history
- logging and attestation

### Legacy API/spec lineage
Move these because they preserve:
- old OF Platform API coverage
- legacy OpenAPI surface
- runtime README
- package/version map

### Legacy semantic lineage
Move these because they preserve:
- early RM semantics
- later agronomy-archetype semantics
- ontology lineage
- external ontology mapping registry
- reference-ingest ideas

## Important naming rule for the new project

In the new project:

- use **OFARM**
- use **OFARM Platform**
- do **not** carry active working directories, top-level docs, or new artifacts under `fa_rm`, `farm_rm`, or `Farm-RM` names

Legacy files can retain those names **inside `legacy_reference/fa_rm_v1/` only**.

## Practical recommendation

Use the packaged folder/zip created alongside this report as the **seed import** for the new OFARM 2 project.

Then:
1. import the active authority/support folders first
2. import the legacy reference folder separately
3. keep legacy reference clearly segregated from authoritative files
4. do not import old intermediate drafts

## Most important decision

The new project should begin from:

- `OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `OFARM_Alignment_Register_v0_13.md`

Everything else should orbit around that.

## Package contents

This seed package includes:
- active baseline
- companion artifacts
- accepted RFCs
- machine contracts
- implementation/conformance artifacts
- handoff/prompts
- curated legacy reference from `fa_rm-1.0.26`

It also includes:
- `README.md`
- `MANIFEST.csv`

## Final recommendation

**Migrate the curated package, not the old repo.**

That gives you:
- continuity
- context
- legacy insight
- implementation scaffolding

without bringing old naming and old clutter back into the center.


---

## Update in v0.3

Added as **ACTIVE_SUPPORTING_RESEARCH** for further OFARM development:

- `06_active_supporting_research/syntheses/OFARM_research_hardest_design_problems_v0_1.md`
- `06_active_supporting_research/syntheses/OFARM_research_Codex_implementation_methodology_v0_1.md`
- `06_active_supporting_research/syntheses/OFARM_research_real_farming_scenarios_v0_1.md`
- `06_active_supporting_research/syntheses/OFARM_research_external_standard_readiness_v0_1.md`
- `06_active_supporting_research/syntheses/OFARM_research_developer_and_AI_agent_UX_v0_1.md`

Added:
- `05_project_handoff_and_prompts/prompts/PROJECT_PROMPT.md`
- `05_project_handoff_and_prompts/prompts/OFARM2_new_project_prompt_v0_1.md`

---

## Update in v0.4

This closure pass repairs the main predevelopment packaging and evidence gaps:

- rebuilt the shipped spike package so the packaged harness can run from package-relative inputs
- regenerated packaged spike run results from the delivered package
- normalized accepted-RFC status metadata and clarified the colocated authority-action matrix classification
- cleaned and realigned the active supporting research files
- added conformance coverage and executable-vs-prose fixture policy artifacts
- added wave-1 machine contracts for PackMergeResolutionTrace, AuthorizationDecisionTrace, MaterializationBasis, and MaterializationSnapshot

The package remains **implementation-directed with bounded debt**, but its evidence and control plane are now substantially cleaner.


---

## Update in v0.5

This closure pass addresses the clearest remaining executable-governance drift point without changing RC2.1 law:

- adds a concrete `PackActivationSet` machine contract derived from the existing Constitution/Platform pack-law sections
- adds a minimal `ActiveArtifactSet` contract so `activeArtifactSetRef` in capability manifests points to a real runtime state object rather than an implied one
- adds pack-activation request/result envelopes and a reusable runtime-problem shape for this seam
- adds executable activation fixtures covering allow, deny, governance-required, and scope-separation outcomes
- adds executable manifest-to-active-artifact-state consistency checks for core and partner deployment examples, including a negative orchard-mismatch case

The package remains **implementation-directed with bounded debt**, but the remaining debt is now narrower:
- broader runtime-boundary envelopes beyond pack activation
- deeper pack/lot/alias conformance breadth
- richer output-taxonomy and authority-sharing executable coverage


---

## Update in v0.6

This closure pass promotes the horizontal external-standard-readiness work into the active authority set without reopening RC2.1 architecture:

- patches the Constitution, Platform, and Pack Safety companion policy narrowly to admit substrate bundles, mapping/loss/runtime-surface contracts, and manifest-by-reference conformance support
- promotes one new companion policy for external-standard role classification
- promotes three accepted RFC extensions covering substrate packaging, interoperability mappings/runtime surfaces, and conformance claim sets
- adds new machine contracts for `SemanticSubstrateBundle`, `MappingCoverageStatement`, `LossMap`, `RuntimeSurfaceContract`, and `ConformanceClaimSet`
- adds a v0.2 draft Capability Manifest schema/example that stays narrow by reference
- adds executable schema validation and consistency checks for the new horizontal contracts

The package still remains **implementation-directed with bounded debt** and **not yet externally standard-ready** for broad bridge-pack claims.
What changed is that the main horizontal law and machine-contract seams for that work are now explicit rather than merely suggested by supporting research.
