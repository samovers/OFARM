# Deep Research Prompt 2 — How to implement OFARM well with Codex and prevent implementation opportunism

You are doing **Deep Research** for **OFARM**, a semantically native crop-farming operating standard and platform architecture that will be implemented heavily with **Codex / LLM-assisted coding systems**.

## Mission
Research the best methodology, papers, engineering practices, and control systems for **successfully implementing OFARM with Codex** while avoiding bad scenarios, including architecture drift, spec erosion, fake completeness, hidden shortcuts, and Codex-related implementation opportunism.

Your job is to identify:
- what can go wrong
- why it goes wrong
- how other teams prevent it
- what a robust implementation method should look like for a project like OFARM

## Baseline you must read first from project files
Read these first:
- `OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `OFARM_reference_implementation_spike_design_notes_v0_1.md`
- `OFARM_conformance_seed_set_v0_1.md`
- `OFARM_implementation_risk_memo_after_spike_v0_1.md`
- `OFARM_reference_spike_harness_run_results_v0_1.json`

Also read the most relevant technical RFCs:
- `OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
- `OFARM_Current_State_Materialization_RFC_v0_1.md`
- `OFARM_QuerySpecification_Schema_RFC_v0_1.md`
- `OFARM_Pack_Merge_Semantics_RFC_v0_1.md`
- `OFARM_Authority_Policy_Model_RFC_v0_1.md`
- `OFARM_Capability_Manifest_RFC_v0_1.md`

## You must explicitly research bad scenarios
List the full failure landscape for an OFARM-like Codex-led project, including but not limited to:

1. **Spec drift**
- code diverges from Constitution / Platform / RFCs
- one implementation path quietly becomes “the truth”

2. **Implementation opportunism**
- writing directly into projections instead of authoritative substrate
- weakening evidence checks
- bypassing pack merge logic
- bypassing authority checks
- treating AI output as de facto governance
- using stale current state for high-consequence flows
- skipping trace objects because they feel inconvenient

3. **Local success / global failure**
- one vertical slice works but the architecture degrades elsewhere
- narrow scenarios validate the wrong shortcuts

4. **Schema theater**
- schemas exist but are not enforced
- manifests exist but are not trusted
- traces exist in prose but not in runtime

5. **Test gap**
- no conformance depth
- fixture sets too shallow
- no invariants around semantic equivalence

6. **Codex-specific failure modes**
- patching the nearest file instead of the right file
- overfitting to current tests
- hallucinated consistency
- aggressive refactors that erase intent
- silent simplification of edge cases
- generating plausible but governance-breaking code
- inventing new concepts instead of using the baseline

7. **Human process failure**
- unclear review ownership
- unclear stop/go criteria
- pressure to ship around the spec
- governance fatigue leading to “temporary” shortcuts

## Research method
- Search for papers and practices on AI-assisted software engineering, specification-driven development, conformance-driven design, model-driven engineering, formal methods where relevant, test oracle design, and socio-technical controls for LLM coding.
- Include research on failure modes of AI coding assistants, code review practices, evals, tool-use constraints, and software quality management.
- Use adjacent domains if useful: safety-critical systems, healthcare software, fintech, infra/platform engineering, regulated ML systems.
- Prefer primary sources and strong engineering writeups over fluff.

## Required output
Produce a report with these sections:

1. **Executive summary**
- the 10 most important implementation-method decisions for OFARM

2. **Failure map**
- bad scenario
- why it would happen in OFARM
- severity
- early warning signs
- strongest prevention mechanism

3. **Recommended implementation methodology**
- planning model
- artifact ownership model
- review model
- branch/PR discipline
- schema/fixture/conformance workflow
- when to use Codex
- when not to use Codex
- how to keep Constitution/Platform/RFCs authoritative

4. **Codex anti-opportunism controls**
- concrete guardrails, checklists, workflows, and automated gates
- what should be enforced in CI
- what should require human review
- what should never be auto-merged

5. **Suggested implementation sequence**
- what to build first
- what to delay
- what to prove with vertical slices
- what to verify with contract harnesses

6. **Research-backed evaluation strategy**
- which evals, traces, fixtures, and conformance suites to build
- how to detect architecture erosion early

7. **Prioritized next actions**
- 10 concrete process or implementation-control actions for OFARM

## Output style
- Be direct and unsentimental.
- Cite the strongest sources.
- Prefer concrete controls over vague principles.
- When research is weak, say so and make the uncertainty explicit.
- Tailor every recommendation to OFARM, not generic AI coding projects.
