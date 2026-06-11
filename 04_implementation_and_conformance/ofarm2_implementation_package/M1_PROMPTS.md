# M1 prompts — copy-paste goal commands

Companion to `M1_BRIEF.md`. One prompt per session; every prompt assumes the session can read the repo. Plan-mode guidance: tasks 1–4 start in plan mode (approve the plan before code); tasks 0, 5–7 run directly.

Boilerplate that opens **every** prompt below (written once here, implied everywhere):

> Read CLAUDE.md, AGENTS.md, DECISIONS.md, M1_BRIEF.md and the files they point to before acting. AGENTS.md rules are binding — privacy rule 1 absolutely. Never weaken a conformance test to make it pass; a wrong-seeming test is an ERRATA.md entry. Extracted contracts are read-only. Paste real command output for every claim of "passing." Before finishing: run `python3 conformance/ofarm_pkg_contract_check.py`, update your task's status in M1_BRIEF.md, append a 5-line entry to WORKLOG.md (what was done, what is red, what is next), commit on your task branch.

---

## Task 0 — environment (no plan mode)

> Execute M1 task 0 on branch `m1/task-0-env`: create `docker-compose.yml` (PostgreSQL 16, named volume, healthcheck), a `Makefile` with `make up`, `make test` (pytest), `make check` (the package self-check), pytest scaffolding under `kernel/tests/`, and `.claude/settings.json` allowlisting `pytest`, `make`, and `docker compose` commands. Create an empty `WORKLOG.md` with a header. Done when: `make up && make test && make check` all succeed on a clean checkout (paste output). Do not start task 1.

## Task 1 — absorb the explainable-evidence RFC (plan mode)

> Execute M1 task 1 on branch `m1/task-1-evidence-design`: read `reference/rfcs/OFARM_Performance_and_Explainable_Current_State_Evidence_RFC_v0_1.md` and all contracts in `contracts/drafts_reference/explainable_current_state_evidence/`. Produce `kernel/DESIGN_MATERIALIZER.md`: how the materializer realizes MaterializationKey, MaterializationFreshnessVector, MaterializationDependencyIndex, and InvalidationEvaluationTrace shapes behind Kernel law (D16: implement, never promote), how basis-set invalidation (D12) maps onto the dependency index, and the table layout consequences for task 2. Design only — no implementation code. Done when the design document answers every "how" in M1_BRIEF task 4 by reference.

## Task 2 — store schema (plan mode)

> Execute M1 task 2 on branch `m1/task-2-store-schema`: PostgreSQL migrations for append-only record tables covering every contract in `contracts/kernel/`, JSONB payloads validated on write against those schemas, explicit edge table for authority/evidence/review/lineage/materialization references, payload sha256 + schemaVersion + schema hash columns, gate-log/outbox table, and the PromotionTrace reachability link written in the same transaction (D3). Append-only enforced in the database (no UPDATE/DELETE grants or triggers raising on both), not just in application code. Done when: migrations apply on clean Postgres; a property test proves UPDATE/DELETE rejection; write-validation rejects an invalid payload; reachability link demonstrated; conformance test 1 and 14 green (paste output). Do not build gates.

## Task 3 — gate pipeline (plan mode)

> Execute M1 task 3 on branch `m1/task-3-gates`: implement the EnforcementChain per PLATFORM.md — ingress normalization; authority gate (default deny, AuthorizationDecision request/result/trace, revocation re-check at sync); validation sub-gates (schema, semantic/carrier, reference-resolution, temporal-conformance, code-binding against `profile_si_ffs/OFARM_AgronomicCodeBindingProfile_si_ffs_v0_1.json`, registry verification against the shipped ReferenceSnapshots); static profile applicability assembling ContextSnapshot from the shipped instances; evidence sufficiency (auto-generated EvidenceSufficiencyCase from the policy template in PROFILE.md); review/promotion implementing self-review per D8. Every refusal is a RuntimeProblem with a reason code, logged. Done when: conformance tests 2, 5, 7, 12, 13 green and the 8 gate-sequencing fixtures replay against the live pipeline (test 4) with pasted results. Do not build the materializer.

## Task 4 — materializer (plan mode)

> Execute M1 task 4 on branch `m1/task-4-materializer`: deterministic materializer per `kernel/DESIGN_MATERIALIZER.md` — in-force records in; CurrentStateMaterialization + complete MaterializationBasis + freshness out; basis-set invalidation (D12: any basis member superseded/revoked/version-bumped, ContextSnapshot component changed, or time policy expired → STALE); dependency index, freshness vector, and InvalidationEvaluationTrace populated per task 1's design. Authority/sharing changes do NOT stale truth — they re-evaluate at read (D12). Done when: conformance tests 8 green, determinism proven by a repeat-run equality test, and a demonstrated STALE transition with its evaluation trace (paste output).

## Task 5 — conformance green (no plan mode)

> Execute M1 task 5 on branch `m1/task-5-conformance`: complete the suite — all 15 tests in conformance/CONFORMANCE.md implemented and green against the live stack, fixtures wired, results emitted as a JSON evidence file under `conformance/results/` (never edited by hand). Any test that cannot pass honestly: leave it red, record why in WORKLOG.md and ERRATA.md if law-related. Done when the suite runs in `make test` and the results file is committed with real timestamps.

## Task 6 — static views (no plan mode)

> Execute M1 task 6 on branch `m1/task-6-views`: author the two QuerySpecification + QueryPlanIR JSON artifacts exactly per views/VIEWS.md against the real store; implement PassportViewMetadata and DocumentAssemblyMetadata emission with ResultQualificationEnvelopes; refusal/disclosure behavior per VIEWS.md (unresolved bindings render as exception rows; STALE bars export; annex never promotes). Done when: conformance tests 9 and 10 green; one end-to-end demo script commits a fictional spray record (use ONBOARDING_RKG_IZPIS.md example values) through the full chain and exports a frozen register (paste its qualification envelope).

## Task 7 — capability manifest (no plan mode)

> Execute M1 task 7 on branch `m1/task-7-manifest`: generate `manifest:si.ffs.pilot.v0_1` from the actual runtime surfaces, declaring every unsupported surface listed in PLATFORM.md; regenerate the ActiveArtifactSet example against the now-real artifacts; verify manifest-vs-artifact-state consistency (test 15, adapt the canonical manifest-grounding pattern). Done when test 15 is green and M1_BRIEF.md's definition-of-done paragraph is demonstrably true end to end — run it and paste the transcript.

---

## Reviewer prompt (fresh session per PR, cloud is fine)

> Review PR <n> with /code-review. Additionally check the diff against KERNEL.md's seven rules and DECISIONS.md D1–D16 and answer explicitly: (1) any weakened or deleted test? (2) any edit to extracted contracts or reference/ files? (3) any file not needed for the task's definition of done? (4) any claim in code comments, docs, or commit messages exceeding the claim limits in AGENTS.md rule 6? (5) any personal data (AGENTS.md rule 1)? Verdict: approve, or itemized blocking findings.

## Deep-session variant (tasks 2→5 in one run — only with a solid local env)

> You have one long session to take the Kernel from empty to conformant. Read CLAUDE.md, AGENTS.md, DECISIONS.md, M1_BRIEF.md, kernel/DESIGN_MATERIALIZER.md. Execute tasks 2, 3, 4, 5 in order on branch `m1/deep-build`, with a hard checkpoint after each task: commit, run `make check` and the task's conformance slice, paste real output, update WORKLOG.md — only then proceed. If a checkpoint cannot pass honestly, stop there and report; never continue on red, never weaken a test. Stop conditions: any contract appears wrong (ERRATA + stop), any ambiguity DECISIONS.md does not settle (stop and ask), context running low (commit + write handoff note + stop). Tasks 0 and 1 must already be merged; do not touch tasks 6–7.

## Resume prompt (any interrupted task)

> Read CLAUDE.md, AGENTS.md, DECISIONS.md, M1_BRIEF.md and WORKLOG.md (last entry). Continue the open task from its branch. Trust the worklog over assumptions; re-run `make check` and the task's tests before changing anything, so you know the true current state. Same definition of done and stop conditions as the original task prompt.
