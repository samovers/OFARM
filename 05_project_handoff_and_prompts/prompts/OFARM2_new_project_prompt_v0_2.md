# OFARM 2 new project prompt v0.2

Status: current CP10 packaged continuity prompt — replace `**[PASTE TASK HERE]**` before use.  
Current in family: `OFARM2_new_project_prompt_v0_2.md`

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
- `02_accepted_rfcs/`
- `01_companion_artifacts/`
- `03_machine_contracts/`

If there is tension inside this authority set, use this internal priority:
1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`

### 2. Active supporting material — supports development, but does not override baseline law
Treat these folders as active supporting material:

- `04_implementation_and_conformance/`
- `06_active_supporting_research/`
- `07_linked_domain_architectures/`
- `05_project_handoff_and_prompts/`

Use them to:
- understand implementation posture
- expand conformance
- plan new work
- improve DX and AI-agent ergonomics
- stress test OFARM with scenarios
- improve standard readiness

These materials do **not** override the baseline by themselves.

### 3. Review holding — reviewed but not active by default
Treat all `reviewed_*` folders as reviewed holding/source-context areas.

Use them when you need:
- reviewed candidate material not silently promoted into active law
- review records, issue registers, and merge decisions
- preserved thread planning and provenance

These materials may inform later work but do **not** override the active authority set.

### 4. Read-only contextualization — lowest authority
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

1. `CURRENT_ACTIVE_ENTRYPOINT.md`
2. `PROJECT_AUTHORITY.md`
3. `ACTIVE_SUBSTANCE_README.md`
4. `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
5. `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
6. `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
7. `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
8. `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

Then read the active accepted RFCs relevant to the task:

9. `02_accepted_rfcs/README.md`
10. the directly relevant files under `02_accepted_rfcs/`

Then read the active companion artifacts relevant to the task:

11. `01_companion_artifacts/README.md`
12. the directly relevant files under `01_companion_artifacts/`

Then read the machine contracts and examples:

13. `03_machine_contracts/README.md`
14. the directly relevant schema-family README, currentness map, schemas, and example maps under `03_machine_contracts/`

Then read active supporting implementation/research materials only as needed:

15. `04_implementation_and_conformance/README.md`
16. `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/README.md`
17. `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/PROMOTION_INDEX.json`
18. `06_active_supporting_research/README.md`
19. `07_linked_domain_architectures/README.md`
20. `05_project_handoff_and_prompts/README.md`

Read review-holding folders only when you have a specific reason. Read `legacy_reference/` only when you have a specific reason.

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
  - explicit evidence sufficiency handling, including degraded and late-evidence posture
  - internal query model with QuerySpecification and QueryPlanIR
  - PassportView / DocumentAssembly taxonomy
  - runtime enforcement chain
  - Capability Manifest as runtime self-description
  - active machine contract families for source truth records, authority source records, context/reference basis, local knowledge/planning objects, and remaining governance objects

- current maturity:
  - **implementation-directed with bounded debt**
  - **AAI-CP10 is the current controlled-promotion endpoint**
  - **CP10 does not claim production readiness, full runtime AI-agent readiness, world-model readiness, farmer UX readiness, live registry integration, or external-standard readiness**
  - **horizontal external-standard-readiness law is explicit**
  - **same-standard bridge promotion remains `DRAFT` until real deployment evidence exists**
  - **a pre-implementation evidence-capture path now exists for future same-standard bridge promotion evidence**
  - **not yet externally standard-ready for broad bridge-pack claims**

---

## How to treat Deep Research and review-holding reports

The files in `06_active_supporting_research/` are meant for **further development of OFARM**.
The files in `07_linked_domain_architectures/` are meant to make the intended adjacent-platform picture explicit without promoting those platforms into active OFARM law.
Use them to inform:
- follow-on RFCs
- conformance expansion
- implementation planning
- developer and AI-agent UX improvements
- scenario stress testing
- standard-readiness work

The files in `reviewed_preimplementation_thread_v0_2/` and `reviewed_regulatory_inspector_thread_v0_1/` are **review-holding materials**.
Use them to:
- recover thread context and reviewed candidate material
- inspect prior issue registers, merge decisions, and thread closure plans
- inform selective future merge work without silently promoting held material into active law

Apply this rule in all cases:
- if a recommendation conflicts with the active baseline, the **baseline wins until explicitly changed**

In other words:
- research informs
- linked-domain framing informs
- review holding informs
- baseline governs

---

## Non-negotiable rules

Do not:
- flatten OFARM into a simple CRUD system
- let projections become hidden truth stores
- let AI outputs become de facto governance decisions
- let sister-platform caches or commercial/social process state become hidden OFARM truth stores
- let packs mutate core meaning
- let stale current state drive high-consequence outputs by default
- let legacy FA_RM / FARM_RM terminology silently re-enter active OFARM 2 law
- use “passport” as a bucket term for every compiled output
- treat package-local rehearsal fixtures or capture templates as live field evidence
- promote same-standard bridge pairs beyond `DRAFT` without real live telemetry, deployment-produced trace-back linkage, and explicit production approval

Always preserve:
- determinism
- traceability
- explicit authority
- explicit evidence policy
- explicit promotion rules
- clear separation between active law and contextual/reference material
- no-edit-in-place posture for frozen outputs and post-submission correction paths

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

When the task touches bridge promotion or external-standard readiness:
1. distinguish package-local proof from deployment evidence
2. keep candidate bridge pairs at their current maturity unless the explicit promotion gate is satisfied
3. do not infer production readiness from templates, synthetic traces, or replayed package fixtures

Now do the task:

**[PASTE TASK HERE]**
