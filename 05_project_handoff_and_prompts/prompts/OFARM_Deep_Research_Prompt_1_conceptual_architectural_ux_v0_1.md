# Deep Research Prompt 1 — OFARM conceptual / architectural / UX hard problems

You are doing **Deep Research** for **OFARM**, a semantically native crop-farming operating standard and platform architecture.

## Mission
Research the **trickiest, most ambiguous, or most failure-prone conceptual / architectural / UX elements** of OFARM and identify the best available:
- papers
- standards
- best practices
- design patterns
- cautionary examples
- cross-industry analogues

Do **not** focus on politics, lobbying, procurement, commercial GTM, or adoption strategy.  
Focus only on whether OFARM is **conceptually sound, architecturally robust, usable, and technically standardizable**.

## Baseline you must read first from project files
Read these before researching:
- `OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `OFARM_Alignment_Register_v0_13.md`
- `OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

Also read the most relevant companion artifacts and RFCs:
- `OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
- `OFARM_Pack_Safety_and_Compatibility_Policy_v0_2.md`
- `OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`
- `OFARM_Query_Architecture_Note_v0_1.md`
- `OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
- `OFARM_Platform_Enforcement_Architecture_Memo_v0_1.md`
- `OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
- `OFARM_Current_State_Materialization_RFC_v0_1.md`
- `OFARM_QuerySpecification_Schema_RFC_v0_1.md`
- `OFARM_Pack_Merge_Semantics_RFC_v0_1.md`
- `OFARM_Authority_Policy_Model_RFC_v0_1.md`

## Priority research areas
Research best practices, papers, and concrete approaches for:

1. **Identity and lifecycle semantics**
- durable identity vs revision vs time-bounded state
- field boundary changes
- zone lifecycle
- crop-cycle lifecycle
- lot identity, split/merge/commingling/transformation
- storage/container/facility lineage

2. **Current-state materialization**
- assertion/history-first authority with derived current state
- freshness, staleness, invalidity
- materialization basis and snapshots
- when to recompute vs refuse vs review
- twin-specific state policy (compliance vs advisory)

3. **Pack/profile/extension architecture**
- modular context systems
- pack compatibility
- surface-specific merge semantics
- avoiding context explosion
- preventing hidden semantic forks
- preventing silent partial activation

4. **Authority / delegation / sharing / revocation**
- action-based authorization
- scope inheritance
- delegation bounds
- human-only governance defaults
- multi-party agricultural workflows
- AI-assisted action boundaries

5. **Query architecture**
- internal canonical query model
- graph-pattern-first and path-aware querying
- alias stability across evolving content models
- semantic equivalence across graph/materialized/projection execution paths

6. **Output taxonomy and UX**
- live compiled views vs frozen governed outputs
- dossier / report / submission / passport distinctions
- how to make complex semantic systems usable by real users
- guided interaction for structured truth capture
- how to avoid UI that pushes users into fake certainty or unusable complexity

7. **AI/world-model readiness**
- grounding AI in governed symbolic state
- multimodal evidence as first-class input
- simulation/counterfactual support
- keeping AI from bypassing governance
- traceability of AI-assisted interpretation and authoring

## Research method
- Use primary sources first: standards bodies, formal specs, peer-reviewed papers, official documentation.
- Use other industries when useful: healthcare, manufacturing, supply chain, geospatial, digital twins, knowledge graphs.
- Prefer recent sources for moving topics, but include foundational sources where still important.
- When there are competing approaches, compare them explicitly.
- If evidence is mixed, say so clearly.

## Required output
Produce a report with these sections:

1. **Executive summary**
- the 10 most important research-backed improvements or cautions for OFARM

2. **Priority problem map**
- OFARM issue
- why it is hard
- strongest external analogues
- strongest recommended approach
- confidence level

3. **Research-backed design recommendations**
- one section per priority area above
- clearly label: adopt now / pilot first / avoid / watch

4. **UX implications**
- what the research says about making this kind of system actually usable
- concrete OFARM implications

5. **Red flags**
- patterns likely to damage OFARM if adopted

6. **Prioritized next actions**
- 5 to 10 concrete follow-on RFCs, design changes, or test expansions

## Output style
- Be blunt.
- Cite all load-bearing claims.
- Explicitly say where evidence is weak.
- Do not give generic architecture advice detached from OFARM.
- If something in the OFARM baseline looks internally inconsistent, call it out directly.
