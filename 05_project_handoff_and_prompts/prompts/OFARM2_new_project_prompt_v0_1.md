# OFARM 2 new project prompt v0.1

Superseded currentness note: this is historical supporting prompt material. For the CP10 package, use `PROJECT_PROMPT.md` or `OFARM2_new_project_prompt_v0_2.md`.


Status: superseded template prompt — retained for lineage only.
Superseded by: `OFARM2_new_project_prompt_v0_2.md`


You are working inside the **new dedicated OFARM 2 project**.

## Your job
Continue OFARM from the **current active migrated baseline**.
Do not restart architecture exploration from scratch.
Do not treat legacy FA_RM / FARM_RM material as active law.
Do not reopen broad design questions unless you can show a real contradiction or a missing executable contract.

Your immediate task is:

**[PASTE TASK HERE]**

---

## Source authority model

### 1. Active substance — highest authority
Treat these folders as the active OFARM 2 authority set:

- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

If there is tension inside this authority set, use this internal priority:
1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`

### 2. Active supporting material — supports development, but does not override baseline law
Treat these folders as active supporting material:

- `04_implementation_and_conformance/`
- `05_project_handoff_and_prompts/`
- `06_active_supporting_research/`

Use them to:
- understand implementation posture
- expand conformance
- plan new work
- improve DX and AI-agent ergonomics
- stress test OFARM with scenarios
- improve standard readiness

These materials do **not** override the baseline by themselves.

### 3. Read-only contextualization — lowest authority
Treat this folder as reference-only contextualization:

- `legacy_reference/`

Use it only when:
- you need historical context
- you need to inspect older OFARM / FA_RM / FARM_RM resources for reusable ideas
- you want to compare the old repo with OFARM 2 decisions

Never let legacy_reference silently overrule the RC2.1 baseline.

---

## Read order

Read in this order before doing serious work:

1. `PROJECT_AUTHORITY.md`
2. `ACTIVE_SUBSTANCE_README.md`
3. `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
4. `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
5. `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
6. `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
7. `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

Then read the active normative support, in this order:

8. `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
9. `01_companion_artifacts/OFARM_Pack_Safety_and_Compatibility_Policy_v0_2.md`
10. `01_companion_artifacts/OFARM_External_Standards_Integration_and_Interoperability_Policy_v0_1.md`
11. `01_companion_artifacts/OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`
12. `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`
13. `01_companion_artifacts/OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
14. `01_companion_artifacts/OFARM_Platform_Enforcement_Architecture_Memo_v0_1.md`

Then read the accepted RFCs that define post-charter closure of the main gaps:

15. `02_accepted_rfcs/OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
16. `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
17. `02_accepted_rfcs/OFARM_QuerySpecification_Schema_RFC_v0_1.md`
18. `02_accepted_rfcs/OFARM_Pack_Merge_Semantics_RFC_v0_1.md`
19. `02_accepted_rfcs/OFARM_Authority_Policy_Model_RFC_v0_1.md`
20. `02_accepted_rfcs/OFARM_Authority_Action_Matrix_v0_1.md` (accepted closure companion artifact colocated with RFC-4)
21. `02_accepted_rfcs/OFARM_Capability_Manifest_RFC_v0_1.md`
22. `02_accepted_rfcs/OFARM_Semantic_Substrate_Bundle_and_External_Profile_Packaging_RFC_v0_1.md`
23. `02_accepted_rfcs/OFARM_Interoperability_Mapping_Coverage_Loss_and_Runtime_Surface_RFC_v0_1.md`
24. `02_accepted_rfcs/OFARM_Conformance_Claim_Set_and_Capability_Manifest_Reference_Extension_RFC_v0_1.md`

Then read the machine contracts and examples:

25. `03_machine_contracts/`

Then read the active supporting research and implementation materials:

26. `06_active_supporting_research/`
27. `04_implementation_and_conformance/`

Then use prompts/handoff materials only if needed:

28. `05_project_handoff_and_prompts/`

Read `legacy_reference/` only when you have a specific reason.

---

## What is currently true about OFARM

Assume all of the following are already decided:

- OFARM has a **model/runtime split**
  - Constitution = model law
  - Platform = runtime law

- canonical truth is **assertion/history-first**
- current state is a **governed materialization**
- there is **one semantic substrate**
- there are two logical twins:
  - Compliance Twin
  - Advisory Twin

- OFARM has:
  - explicit event grammar
  - explicit commit classes and promotion law
  - explicit pack law
  - explicit authority / delegation / revocation law
  - internal query model with QuerySpecification and QueryPlanIR
  - PassportView / DocumentAssembly taxonomy
  - runtime enforcement chain
  - Capability Manifest as runtime self-description

- current maturity:
  - **implementation-directed with bounded debt**
  - **horizontal external-standard-readiness law is now explicit**
  - **not yet externally standard-ready for broad bridge-pack claims**

---

## How to treat the Deep Research reports

The files in `06_active_supporting_research/` are meant for **further development of OFARM**.

Use them to inform:
- follow-on RFCs
- conformance expansion
- implementation planning
- developer and AI-agent UX improvements
- scenario stress testing
- standard-readiness work

But apply this rule:
- if a report recommendation conflicts with the active baseline, the **baseline wins until explicitly changed**

In other words:
- research informs
- baseline governs

---

## Non-negotiable rules

Do not:
- flatten OFARM into a simple CRUD system
- let projections become hidden truth stores
- let AI outputs become de facto governance decisions
- let packs mutate core meaning
- let stale current state drive high-consequence outputs by default
- let legacy FA_RM / FARM_RM terminology silently re-enter active OFARM 2 law
- use “passport” as a bucket term for every compiled output

Always preserve:
- determinism
- traceability
- explicit authority
- explicit evidence policy
- explicit promotion rules
- clear separation between active law and contextual reference

---

## Preferred working mode

When proposing change:
1. say which active baseline files are affected
2. say whether the change is:
   - baseline law
   - RFC extension
   - supporting research implication
   - implementation/conformance implication
3. state risks clearly
4. propose the smallest controlled patch rather than a fresh rewrite

Now do the task:

**[PASTE TASK HERE]**
