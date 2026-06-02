# Deep Research Prompt 4 — External standard readiness: which standards OFARM should include, profile, align to, or avoid

You are doing **Deep Research** for **OFARM**, a semantically native crop-farming operating standard and platform architecture.

## Mission
Research how OFARM can become **more externally standard-ready** in the technical sense.

Your job is to determine:
- which standards, ontologies, profiles, and formal artifacts OFARM should **include**, **profile**, **align to**, **reuse**, or **avoid**
- how to structure those relationships so OFARM becomes easier to interoperate with without becoming a thin wrapper around other people’s models
- where OFARM should stay OFARM-owned

Focus only on:
- technical / semantic / architectural / formal interoperability readiness

Do **not** focus on:
- politics
- standards-body strategy
- lobbying
- procurement
- commercial adoption strategy

## Baseline you must read first from project files
Read these first:
- `OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `OFARM_Alignment_Register_v0_13.md`
- `OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

Also read these standards-sensitive artifacts:
- `OFARM_Query_Architecture_Note_v0_1.md`
- `OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
- `OFARM_Pack_Safety_and_Compatibility_Policy_v0_2.md`
- `OFARM_Capability_Manifest_RFC_v0_1.md`
- `OFARM_QuerySpecification_Schema_RFC_v0_1.md`
- `OFARM_Pack_Merge_Semantics_RFC_v0_1.md`
- `OFARM_Authority_Policy_Model_RFC_v0_1.md`
- `OFARM_Current_State_Materialization_RFC_v0_1.md`
- `OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`

## Priority questions to answer
Research and answer, with evidence:

1. **Semantic-core standards**
- What should OFARM formally profile or align to for shared ag semantics?
- What is the strongest current role of AIM?
- Where should OFARM reuse vs profile vs align vs stay independent?

2. **Cross-domain standards**
- geospatial
- time
- units
- provenance
- observation / sensor semantics
- eventing
- query/filtering
- traceability
- document/attestation
- capability self-description
- digital-twin / submodel patterns

3. **Exchange and integration surfaces**
- ADAPT
- AEF / ISOXML / EFDI
- NGSI-LD / FIWARE
- SAREF4Agri
- EPCIS or related traceability/event standards
- any other standards that are strong candidates and worth serious inclusion

4. **Query and filter readiness**
- what should OFARM learn from SPARQL, AQL, CQL2, OGC API filtering, or similar
- how much should OFARM profile versus invent

5. **Capability / manifest / discovery readiness**
- what standards or patterns should inform Capability Manifest and registry/discovery behavior

6. **What to avoid**
- standards that look attractive but would likely weaken OFARM if made canonical in the wrong place
- places where OFARM should stay OFARM-owned

7. **How to package standard readiness**
- profile strategy
- binding strategy
- mapping strategy
- conformance-claim strategy
- loss-map / coverage-statement strategy

## Research method
- Use primary sources first: formal standards, official specifications, official repositories, standards bodies, peer-reviewed papers where available.
- Use current sources; verify whether active standards or repos have evolved.
- Compare multiple candidate standards where overlap exists.
- Distinguish:
  - semantic anchor
  - runtime surface
  - exchange format
  - profile layer
  - implementation convenience

## Required output
Produce a report with these sections:

1. **Executive summary**
- the 10 most important standard-readiness conclusions for OFARM

2. **Standards landscape map**
For each candidate standard / ontology / profile:
- what it is good for
- what layer it belongs to
- whether OFARM should reuse, profile, align, wrap, or avoid it
- confidence level

3. **Recommended OFARM standard stack**
- what belongs in shared semantic substrate
- what belongs in OFARM-owned operational/compliance layer
- what belongs in runtime/integration layer
- what belongs only as mapping/profile surface

4. **Formal inclusion strategy**
- how OFARM should technically include or reference the chosen standards
- where formal profiles or bindings should exist
- where loss maps / coverage statements are necessary
- what conformance claims would make sense

5. **Red flags**
- standards that could damage OFARM if adopted too deeply or at the wrong layer

6. **Prioritized next actions**
- 5 to 10 concrete standard-readiness tasks, profiles, or RFCs

## Output style
- Be blunt.
- Use citations for all load-bearing claims.
- Distinguish clearly between:
  - “must include now”
  - “profile soon”
  - “align only”
  - “map only”
  - “avoid for now”
- Do not recommend standards just because they are famous.
- Judge them by OFARM’s actual architecture.
