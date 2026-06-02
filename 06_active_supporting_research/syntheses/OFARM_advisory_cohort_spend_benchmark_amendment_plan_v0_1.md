# OFARM advisory cohort spend benchmark amendment plan v0.1

Date: 2026-04-14
Status: planning packet for critical evaluation before any pre-implementation work
Scope: research plan and pre-implementation plan for a bounded OFARM capability that lets a user see cohort-level benchmark spending for a normalized fertilizer or seed product or governed product class, using receipt-backed data already present in the system

---

## 1. Recommendation

Treat this as a **bounded Advisory-Twin cohort benchmark capability**, not as direct tenant-to-tenant visibility and not as a new constitutional architecture round.

The first wave should stay in:
- `06_active_supporting_research/`
- `04_implementation_and_conformance/`
- narrowly targeted companion clarification in `01_companion_artifacts/` only if the critical review says the policy seam is clear enough

It should **not** start with baseline-law patches, new accepted RFCs, or new machine-contract promotions.

Why:
- `SharingGrant` already governs visibility/use rather than authorship or decision authority, and the Constitution already places cross-farm/regional intelligence in the Advisory Twin by default (`00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`, lines 630-642).
- The Platform already requires explicit sharing, farm/tenant boundary enforcement, and governed pathways for regional/cross-farm intelligence, and it already names benchmark/explainability services as Advisory runtime services (`00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, lines 908-914 and 641-647).
- The authority policy already says there is no implicit cross-farm sharing and recommends opt-in plus aggregation/pseudonymization for regional intelligence (`01_companion_artifacts/OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`, lines 137-153).
- The economics seam is still only companion + implementation work, with a `PARTIAL_PASS` gate and bounded authority/sharing proof (`04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_acceptance_gate_report_v0_1.md`, lines 9-23).

---

## 2. Capability statement to evaluate

### 2.1 Working capability name
**Advisory Cohort Spend Benchmark**

### 2.2 First-wave user outcome
A tenant/farm user may view a governed benchmark for a normalized fertilizer or seed product, or for a governed product class, based on opted-in receipt-backed invoice-line extracts contributed by other participants, with disclosure controls, basis disclosure, and no raw tenant data exposure.

### 2.3 Hard boundaries
The capability must be:
- Advisory only
- query/view first, not scenario first by default
- explicit-share only
- cohort-level only
- disclosure-controlled
- evidence-postured
- revocable for future use
- traceable back to basis and normalization decisions

The capability must **not** become:
- direct row-level cross-tenant visibility
- farm-level compliance truth
- a second query language
- a second truth store
- a new passport family
- a procurement, accounting, or ERP subsystem

These boundaries align with the advisory workspace note, the economics pack note, and the output-taxonomy addendum (`01_companion_artifacts/OFARM_Advisory_Scenario_Workspace_and_Bridge_Note_v0_2.md`, lines 167-249; `01_companion_artifacts/OFARM_Economic_Intelligence_Pack_Note_v0_2.md`, lines 203-260; `01_companion_artifacts/OFARM_Advisory_Scenario_and_Economic_Output_Taxonomy_Addendum_v0_2.md`, lines 27-89).

---

## 3. Affected files and change type

### 3.1 Files affected immediately by the planning/evaluation wave

#### Active supporting research
- new research memo in `06_active_supporting_research/`

#### Active supporting implementation/conformance
- new bounded benchmark package in `04_implementation_and_conformance/`
- new fixtures, redacted datasets, validation runners, hostile tests, and example saved-query/view definitions

#### Companion artifacts, only if critical review approves policy framing
- likely new note: `01_companion_artifacts/OFARM_Advisory_Cohort_Benchmark_and_Disclosure_Control_Policy_v0_1.md`
- possible narrow patch to `01_companion_artifacts/OFARM_Economic_Intelligence_Pack_Note_v0_2.md`
- possible narrow patch to `01_companion_artifacts/OFARM_Advisory_Scenario_and_Economic_Output_Taxonomy_Addendum_v0_2.md`

### 3.2 Files not to patch in the first wave
- `00_active_baseline/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

This matches the current economics promotion posture and the day-0 anti-checklist (`04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_promotion_gate_and_stop_rules_v0_1.md`, lines 24-39; `04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_day0_operator_checklist_v0_1.md`, lines 22-29).

### 3.3 Change classification
- **Primary classification now:** supporting research implication + implementation/conformance implication
- **Possible narrow next step:** companion-artifact clarification
- **Not justified yet:** baseline-law change or new RFC

---

## 4. Core design stance for the research wave

### 4.1 Query/view first, not scenario first
This use case is primarily a governed benchmark retrieval/view problem, not a scenario problem.

The first wave should therefore try to realize the capability through:
1. `QuerySpecification`
2. `QueryPlanIR`
3. governed execution
4. `SUMMARY_ROWS` and/or `VIEW_MODULE`
5. optional frozen `ReportAssembly` for a reviewable packet

That is consistent with the query architecture note and query RFC (`01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`, lines 53-67 and 104-112; `02_accepted_rfcs/OFARM_QuerySpecification_Schema_RFC_v0_1.md`, lines 132-139). The shipped query schema already supports `COUNT`, `MIN`, `MAX`, `SUM`, and `AVG`, and can emit `SUMMARY_ROWS` or `VIEW_MODULE` result modes (`03_machine_contracts/schemas/query/OFARM_QuerySpecification_schema_v0_1.json`, lines 705-743 and 825-840).

### 4.2 First-wave benchmark semantics should not default to raw total spend
“Other tenants spent X” is both weakly comparable and more disclosure-prone than safer benchmark forms.

The research wave must decide a very small allowed benchmark family, likely centered on:
- price per normalized unit
- spend per declared agronomic unit where linkage exists
- quantity bands
- cohort-relative position or banding

The first wave should explicitly avoid assuming that raw total spend is the default metric.

### 4.3 Product identity must be governed and traceable
Receipt-backed data is present, but “specific fertilizer or seed” is not safe as a raw OCR string. The research wave must define how a line item becomes a governed normalized product or product class, with ambiguity/refusal rules.

### 4.4 Disclosure control is the missing seam
The active authority policy reaches opt-in + aggregation/pseudonymization, but I do not see an active contract that defines minimum cohort size, dominant-contributor rules, anti-differencing restrictions, or safe filter narrowing. That is the main amendment seam.

---

## 5. Research workstreams for critical evaluation

## R1. Capability framing and terminology

### Questions to answer
- What is the contribution unit: tenant, farm, declared participant, or scoped data-sovereignty owner?
- What is the benchmark grain: exact normalized product, governed product class, active-ingredient class, seed hybrid family, or something broader?
- What is the eligible window: receipt date, posting date, season window, or declared benchmark window?
- What metric family is actually meaningful and safe?

### Deliverables
- `06_active_supporting_research/syntheses/OFARM_research_advisory_cohort_benchmark_capability_v0_1.md`
- one-page capability statement
- one-page non-goals and anti-drift statement
- open-questions register

### Exit condition
A bounded capability statement exists that reviewers can accept, narrow, or reject without reopening architecture.

---

## R2. Governance, grant topology, and revocation research

### Questions to answer
- Can existing `SHARE_GRANT_ACCESS` + `RECEIVE_READ_DATA` model this safely, or is pooled benchmark use underspecified?
- Who receives the contribution grant: a benchmark operator/service Party, a deployment-owned cohort intelligence service, or another explicit grantee?
- Does the viewer receive only the aggregate view, never the constituent lines?
- How does revocation affect future benchmark recompute, cached views, and previously frozen reports?

### Required outcomes
Define a minimal grant topology with at least:
- contribution grant
- benchmark-view access grant
- revocation behavior
- reason-code taxonomy for denial/refusal

### Deliverables
- grant-topology memo
- decision table for `ALLOW` / `DENY` / `REQUIRE_REVIEW`
- candidate problem codes such as:
  - `NO_BENCHMARK_CONTRIBUTION_GRANT`
  - `BENCHMARK_VIEW_NOT_SHARED`
  - `BENCHMARK_CONTRIBUTION_REVOKED`
  - `BENCHMARK_SCOPE_NOT_AUTHORIZED`

### Exit condition
Reviewers agree that the feature can be modeled without inventing a new constitutional authority family.

The current authority model already provides the needed baseline action classes and traces (`02_accepted_rfcs/OFARM_Authority_Policy_Model_RFC_v0_1.md`, lines 160-182 and 322-345; `02_accepted_rfcs/OFARM_Authority_Action_Matrix_v0_1.md`, lines 23-28).

---

## R3. Disclosure-control and anti-reidentification research

### Questions to answer
- What is the minimum cohort size for showing any result?
- Must contributor count be exact, banded, or hidden?
- What dominance rule blocks exposure when one contributor drives too much of the result?
- Which metrics are disallowed even if the query engine could compute them?
- How do we prevent differencing attacks across near-identical filters?
- What filter dimensions are safe to combine, and how many at once?

### First-wave expectation
The first wave should define a deterministic disclosure-control policy covering at least:
- minimum distinct contributors
- dominant-share threshold
- repeated slicing / differencing guard
- safe filter whitelist
- withholding/suppression reason codes
- fallback to broader product class or refusal

### Deliverables
- hostile privacy/disclosure memo
- benchmark disclosure policy draft
- suppression and refusal examples

### Exit condition
The capability is evaluable as a deterministic governance surface, not as “anonymize and hope.”

---

## R4. Product normalization and comparability research

### Questions to answer
- How do OCR strings, vendor labels, and invoice text become a governed normalized product reference?
- When is the system allowed to resolve to an exact product versus a broader product class?
- How are packaging differences, units, discounts, tax, freight, and bundled lines handled?
- For fertilizer, do comparable views need nutrient-normalized or formulation-normalized posture?
- For seed, do comparable views need seed-count, treatment, variety, or hybrid family posture?

### Recommendation to evaluate
Keep extraction and normalization separate.

A receipt-backed line should remain an extract-shaped line item. Product normalization should be represented as a traceable interpretation layer rather than silently embedded as raw fact.

### Deliverables
- product-normalization strategy memo
- decision on one of two implementation directions:
  - **Option A:** extend the experimental `ImportedFactExtract` line item with optional normalized product refs and normalization traces
  - **Option B:** keep `ImportedFactExtract` unchanged and add a separate experimental normalization trace object in `04`
- redacted fertilizer and seed line-item example set

### Exit condition
Reviewers agree on a smallest acceptable normalization approach and explicit ambiguity/refusal behavior.

The current experimental `ImportedFactExtract` schema already supports `INVOICE_LINE_SUMMARY` with `lineItems`, `amount`, `quantity`, `unit`, and `evidenceRef`, which is enough to start the research without pretending the product normalization seam is already solved (`04_implementation_and_conformance/spikes_incubation/ofarm_economic_intelligence_spike_v0_1/experimental_machine_contracts/schemas/OFARM_ImportedFactExtract_schema_v0_1.json`, lines 22-30 and 54-74).

---

## R5. Evidence posture and import-path research

### Questions to answer
- What is the minimum path from receipt scan to benchmark contribution?
- Where is human review required after OCR?
- How are duplicates, returns, credit notes, or corrected receipts handled?
- What evidence class does each benchmark metric carry?
- What freshness and as-of semantics attach to a benchmark result?

### Required trace chain
The research packet must specify an end-to-end trace like:
1. receipt/image/document captured as evidence
2. OCR/parse used only as helper
3. reviewed invoice-line summary extracted
4. normalization decision applied
5. benchmark contribution included or refused
6. benchmark view generated with evidence class and freshness posture

### Deliverables
- evidence/import-path memo
- example end-to-end lineage records
- refusal cases for weak OCR, ambiguous product, and unsupported units

### Exit condition
Reviewers agree that the capability preserves document-first and evidence-first posture.

This is aligned with the Platform’s document-first scanner posture and the economics evidence rules (`00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, lines 330-336; `01_companion_artifacts/OFARM_Economic_Intelligence_Pack_Note_v0_2.md`, lines 126-142).

---

## R6. Query, materialization, and freshness research

### Questions to answer
- Can the first wave be expressed with existing query schema subsets, or does it immediately require unsupported group-by/window semantics?
- What saved-query templates are enough for the first wave?
- Which execution targets are allowed for this seam?
- What invalidates a benchmark materialization: new contribution, revoked share, normalization change, currency basis change, or filter-policy change?

### First-wave recommendation
Intentionally constrain the first wave so it does **not** depend on the part of query law that the RFC still leaves open.

That means:
- one product or product class per request
- one declared time window
- one governed cohort filter set
- one or a few aggregate metrics
- shaped output via `SUMMARY_ROWS` or a dedicated `ViewModule`
- no arbitrary multi-product pivoting
- no arbitrary trend windowing
- no percentile/distribution promises in the first wave

### Deliverables
- saved query template set
- bounded query subset note
- freshness/invalidation note

### Exit condition
The first-wave capability is implementable with current query law plus bounded view logic, not by reopening query architecture.

The query RFC itself says v0.1 does not yet solve every future aggregate/group-by/windowing feature, so the first wave must stay within the already-shipped subset (`02_accepted_rfcs/OFARM_QuerySpecification_Schema_RFC_v0_1.md`, lines 193-207).

---

## R7. Output taxonomy and user explanation research

### Questions to answer
- What is the live output family?
- What is the frozen output family if a user exports or shares the result?
- What basis disclosure fields must always be visible to the user?
- How should suppression/refusal appear in UX?

### First-wave mapping recommendation
- live benchmark = `VIEW_MODULE` or `SUMMARY_ROWS`
- optional frozen export = `ReportAssembly`
- no new “economic passport” family
- `PassportView` only if a later use case is truly a concise scope summary and not a cohort decision packet

### Deliverables
- output mapping note
- explanation-field checklist, including:
  - target product/product-class posture
  - cohort eligibility statement
  - evidence class posture
  - freshness state
  - direct vs derived/allocated posture
  - suppression reason where relevant

### Exit condition
Reviewers agree that the output family remains taxonomically clean.

This follows both the Constitution and the economics taxonomy addendum (`00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`, lines 996-1020; `01_companion_artifacts/OFARM_Advisory_Scenario_and_Economic_Output_Taxonomy_Addendum_v0_2.md`, lines 27-89).

---

## R8. Hostile test and stop-rule design

### Must-cover hostile cases
- small cohort reveals likely contributor identity
- one dominant contributor drives most of the benchmark
- repeated filter narrowing allows differencing
- exact product request falls below safe cohort, broader class remains safe
- raw receipt/evidence request is denied even when benchmark view is allowed
- revoked contributor remains in stale cached benchmark
- stale benchmark reused for high-consequence export
- OCR ambiguity creates false exact-product cohorting
- duplicate receipts inflate spend
- refund/credit lines create misleading spend without normalization
- mixed currency or unit makes comparison false
- same tenant multi-farm data accidentally counts as multiple contributors

### Deliverables
- hostile test matrix
- pass/fail acceptance gate for this amendment seam
- explicit cut-back triggers

### Exit condition
The review packet includes enough hostile structure that reviewers can reject the capability on safety grounds before any implementation optimism takes over.

---

## 6. Critical evaluation gate

No pre-implementation work should start until reviewers have a packet with these exact items:

1. bounded capability statement
2. grant-topology decision memo
3. disclosure-control proposal
4. product-normalization proposal with chosen smallest patch direction
5. first-wave query subset and saved-query templates
6. output mapping note
7. hostile test matrix
8. go / narrow / stop recommendation

### Review questions
The critical review should answer:
- Is this still clearly Advisory-only?
- Is the feature query/view-first rather than a hidden second scenario/query system?
- Does the grant topology stay inside current authority law?
- Is disclosure control explicit enough to be enforceable?
- Is the product-normalization seam traceable and non-magical?
- Does the first wave avoid unsupported analytical features?
- Does the output taxonomy stay inside `ViewModule` / `ReportAssembly` law?
- Does the value come mostly from already-captured receipt-backed data rather than new manual finance burden?

### Allowed review outcomes
- **Proceed as bounded 01 + 04 adjunct work**
- **Proceed as 04-only experiment with no new companion artifact yet**
- **Cut back to broader product-class or own-history-only benchmarking**
- **Stop**

---

## 7. Pre-implementation plan, only after critical approval

## P1. Companion-artifact patch set

### Recommended target
A new narrow companion artifact in `01_companion_artifacts/`:

`OFARM_Advisory_Cohort_Benchmark_and_Disclosure_Control_Policy_v0_1.md`

### What it should define
- capability scope
- explicit opt-in contribution posture
- grant topology
- disclosure-control rules
- safe metric families
- product normalization posture
- revocation behavior
- output family mapping
- hard anti-drift rules

### Optional narrow companion patches
Only if needed after review:
- patch `OFARM_Economic_Intelligence_Pack_Note_v0_2.md` to add explicit cohort benchmark examples and first-wave ViewModules
- patch `OFARM_Advisory_Scenario_and_Economic_Output_Taxonomy_Addendum_v0_2.md` to include a benchmark report example

### What not to do
Do not patch the Constitution, Platform, or Alignment Register in this wave unless the critical review proves an actual missing constitutional contract.

---

## P2. Experimental contracts and example objects in `04`

### Required artifacts
- redacted multi-participant benchmark sample dataset for fertilizer and seed cases
- saved-query examples for:
  - exact normalized product benchmark where safe
  - product-class fallback benchmark
  - price-per-unit benchmark
  - spend-per-ha benchmark where operational linkage exists
- `ViewModule` examples for user-facing benchmark cards/tables
- optional frozen `ReportAssembly` example

### Candidate schema work in `04`, not `03`
Depending on the research decision:
- **Option A:** minimal experimental patch to `ImportedFactExtract`
- **Option B:** new experimental normalization-trace object and optional benchmark-contribution object

### Strong recommendation
Prefer the smallest patch that preserves raw-versus-interpreted discipline.

---

## P3. Runtime decision fixtures and validators

### New fixture families
- contribution-share allow/deny fixtures
- benchmark-view access allow/deny fixtures
- revocation recheck fixtures
- suppression and small-cohort refusal fixtures
- no-raw-evidence-access fixtures
- stale benchmark recompute/refusal fixtures
- filter-narrowing denial fixtures
- normalization ambiguity review/refusal fixtures

### New runner outputs
- benchmark authorization decision records
- benchmark disclosure decision records
- benchmark freshness and invalidation records
- benchmark output trace-back records
- hostile test result summary

### Minimum expected reason codes
At minimum the seam should be able to emit codes like:
- `NO_IMPLICIT_CROSS_FARM_SHARING`
- `BENCHMARK_INSUFFICIENT_COHORT`
- `BENCHMARK_DISCLOSURE_RISK`
- `BENCHMARK_PRODUCT_AMBIGUOUS`
- `BENCHMARK_NONCOMPARABLE_UNIT`
- `BENCHMARK_CONTRIBUTION_REVOKED`
- `BENCHMARK_MATERIALIZATION_STALE`

The existing sharing-boundary fixtures and runtime records are a good base but are not yet benchmark-specific (`04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_Runtime_Authority_Action_Class_and_Sharing_Boundary_Fixtures_v0_1.md`, lines 57-86; `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_runtime_sharing_boundary_access_records_v0_1.json`, lines 100-113).

---

## P4. Redacted pilot packet

### Goal
Create one bounded redacted pilot packet that proves the seam with already-present receipt-backed data, without requiring broad new finance entry.

### Contents
- redacted receipt/invoice evidence refs
- reviewed invoice-line summaries
- normalization traces
- benchmark cohort membership declarations
- query outputs
- suppression/refusal cases
- one exportable report example

### Redaction rule
Use the existing redaction/sovereignty posture as the base: stable redacted refs, no unnecessary personal/bank/raw invoice export, farm-private by default, advisory storage only (`04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_real_farm_pilot_redaction_and_sovereignty_note_v0_1.md`, lines 7-33).

---

## P5. Conformance update and promotion check

### Required update set
- add the benchmark seam to `OFARM_conformance_seed_set_v0_1.md`
- add a new row or sub-row in the conformance matrix
- add a benchmark-specific hostile review memo
- add a benchmark-specific acceptance gate report

### Promotion posture after pre-implementation
Even after successful pre-implementation, keep the seam in `01 + 04` unless all promotion thresholds are met:
- deployment-shaped proof
- stronger projection trace-back
- target-equivalence proof for used execution targets
- non-curated authority/sharing proof
- generic seam justification

That threshold is already stated for the economics seam (`04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_promotion_gate_and_stop_rules_v0_1.md`, lines 24-39).

---

## 8. Risks

### RISK 1 — “Anonymized” becomes a false safety label
The plan fails if it substitutes pseudonym removal for real disclosure control.

### RISK 2 — Product normalization silently becomes a second schema
The plan fails if OCR strings, vendor labels, or heuristic mappings become hidden truth without governed traces.

### RISK 3 — Query convenience reopens query architecture
The plan fails if multi-dimensional cohort analytics forces ad hoc group-by/window logic outside `QuerySpecification` and `QueryPlanIR`.

### RISK 4 — Cached aggregate views act like truth stores
The plan fails if benchmark caches become de facto authoritative state rather than governed Advisory outputs.

### RISK 5 — Revocation is not reflected in future views
The plan fails if a contributor revokes sharing but remains in visible benchmark aggregates without explicit retention policy.

### RISK 6 — Output drift creates a fake “economic passport”
The plan fails if benchmark cards or exported summaries are relabeled as a new passport family.

---

## 9. Stop conditions

Stop or cut back the amendment if any of these become true during the research or pre-implementation wave:
- benchmark use requires baseline-law changes just to get started
- safe disclosure control cannot be stated deterministically
- exact-product normalization is too ambiguous to govern reliably
- first-wave value depends on unsupported group-by/window features
- broad manual finance-entry burden appears
- the feature keeps drifting toward ledger/procurement semantics
- the only workable UX exposes low-cardinality cross-tenant slices

These are consistent with the economics seam stop rules already in force (`04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_promotion_gate_and_stop_rules_v0_1.md`, lines 9-20).

---

## 10. Bottom line

The smallest controlled path is:

1. research the capability as a **bounded Advisory cohort benchmark seam**
2. keep the first wave **query/view-first**
3. solve **grant topology + disclosure control + product normalization** before coding
4. keep the first implementation wave in **01 + 04**, with **no 00/02/03 promotion**
5. use a **critical evaluation gate** before any pre-implementation work starts

That path is consistent with the current OFARM authority set, with the existing economics promotion posture, and with the instruction not to reopen architecture unless a real missing constitutional contract appears.
