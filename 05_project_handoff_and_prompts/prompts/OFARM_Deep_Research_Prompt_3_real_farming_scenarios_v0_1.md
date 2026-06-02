# Deep Research Prompt 3 — Real-life staple crop farming scenarios to stress test OFARM before implementation

You are doing **Deep Research** for **OFARM**, a semantically native crop-farming operating standard and platform architecture.

## Mission
Research **real-life staple crop farming scenarios** across the full operating reality of crop farming, especially:
- common routine scenarios
- messy edge cases
- multi-party scenarios
- scenarios that are likely to be heavy or failure-prone for OFARM

The goal is to build a **stress-test scenario base** before implementation.

This is not just agronomy research.  
It is scenario research for:
- operational modeling
- evidence handling
- traceability
- compliance
- authority
- outputs
- current-state freshness
- pack/context interactions
- failure modes in real-world farming practice

## Baseline you must read first from project files
Read these first:
- `OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `OFARM_Alignment_Register_v0_13.md`
- `OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

Read these scenario-sensitive companion artifacts:
- `OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
- `OFARM_Pack_Safety_and_Compatibility_Policy_v0_2.md`
- `OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`
- `OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
- `OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
- `OFARM_Current_State_Materialization_RFC_v0_1.md`
- `OFARM_Pack_Merge_Semantics_RFC_v0_1.md`
- `OFARM_Authority_Policy_Model_RFC_v0_1.md`

## Scope of farming reality to cover
Focus on **staple crop farming**, but cover the full practical reality around it. Include:
- cereals
- oilseeds
- maize/corn
- pulses/legumes where relevant
- mixed rotations
- storage and post-harvest handling
- contractor work
- buyer / certifier / inspector interactions
- subsidies/support paperwork where relevant
- damage / contamination / insurance / dispute contexts where relevant

## Scenario categories you must research
Produce real-world scenario families for at least:

1. **Planning and establishment**
- field preparation
- sowing/planting
- replanting
- seed changes
- failed establishment
- overlapping or split crop cycles

2. **Routine operations**
- fertilization
- crop protection
- irrigation where relevant
- cultivation / tillage / mowing / cover-crop handling
- contractor-executed operations
- machine-generated work records vs human-reported work

3. **Observation and decision**
- scouting
- disease / pest suspicion vs confirmation
- weak signals
- local heuristics
- microclimate effects
- remote-sensing or advisory triggers
- contradictory observations

4. **Harvest and post-harvest**
- harvest batches
- wet grain
- temporary storage
- drying
- cleaning
- lot creation / split / merge
- contamination risk
- transport
- buyer delivery
- claim/certificate preservation

5. **Compliance and inspection**
- organic segregation
- buffer zones
- unsupported claims
- missing evidence
- certifier inspection
- nonconformity and corrective action
- subsidy/support filing
- inspection dossiers
- submissions

6. **Authority and sharing**
- owner vs operator
- advisor-assisted actions
- contractor reporting
- buyer read-only access
- certifier review powers
- revoked access after draft work
- AI-assisted preparation that still requires human approval

7. **Heavy / ugly scenarios**
- commingled lots
- uncertain boundary changes
- crop failure and replant
- late evidence arrival
- stale current-state used in a sensitive flow
- conflicting packs on the same scope
- partially missing machine records
- evidence that exists but is low quality
- one farm with mixed conventional and organic contexts
- dispute over whether a lot is still the same lot
- correction/supersession after a submission was already assembled

## Research method
- Use authoritative agronomy extension material, crop-management guides, post-harvest handling references, crop-protection guidance, regulatory guidance where relevant, and practical farm management sources.
- Use sources from multiple regions where useful, but keep the focus on scenario realism rather than market differences.
- Prefer scenario-rich, operational sources over abstract agronomy summaries.
- Where practices differ materially by crop or region, say so.

## Required output
Produce a report with these sections:

1. **Executive summary**
- the 10 most important scenario findings for stress-testing OFARM

2. **Scenario inventory**
For each scenario, include:
- scenario name
- operational context
- key actors
- key objects (field, lot, cycle, container, evidence, etc.)
- likely event families
- likely commit classes
- likely pack/context interactions
- likely current-state / freshness issues
- likely outputs (passport, report, dossier, submission)
- why it is hard for OFARM

3. **Top stress-test scenarios**
- identify the 15 to 25 scenarios most likely to break a weak implementation

4. **Scenario clusters by OFARM risk**
- identity/lifecycle risk
- current-state freshness risk
- pack merge risk
- authority risk
- evidence risk
- output taxonomy risk
- query / retrieval risk

5. **What must be added to conformance fixtures**
- concrete scenario-driven test requirements

6. **What OFARM already handles well vs weakly**
- based on the current RC2.1 baseline

7. **Prioritized next actions**
- specific scenario-driven design or test expansions

## Output style
- Be concrete and operational.
- Use citations.
- Do not drift into generic agronomy explanation unless it helps scenario stress testing.
- Point out which scenarios are common and which are rare-but-dangerous.
- Treat “messy but common” as more important than exotic edge cases.
