# OFARM advisory cohort spend benchmark plan — critical evaluation v0.1

Date: 2026-04-14
Status: critical evaluation of the planning packet before any pre-implementation work
Scope: evaluate `06_active_supporting_research/syntheses/OFARM_advisory_cohort_spend_benchmark_amendment_plan_v0_1.md` against the active OFARM authority set and determine whether pre-implementation should proceed, be narrowed, or stop

---

## 1. Verdict

**Proceed, but narrow.**

The planning packet is directionally correct on constitutional placement, twin placement, sharing posture, output taxonomy, and anti-ERP boundaries.

It is **not yet safe to execute as written** because two seams are still under-specified at the executable level:

1. **disclosure control** for cross-tenant benchmark outputs
2. **aggregate/query shape** needed to compute contributor-count and dominance rules without reopening query law

### Review outcome

**Proceed as `04`-only experiment with no new companion artifact yet.**

That is the smallest controlled path.
A narrow companion-artifact policy note may follow **only after** the disclosure and benchmark-shaping rules are proven in executable `04` artifacts.

### Why this is the right outcome

The active baseline already supports:
- explicit sharing rather than silent cross-party access
- Advisory-Twin placement for cross-farm/regional intelligence
- query/view-first realization
- non-ledger imported finance extracts
- live view vs frozen report taxonomy

But the hostile review and readiness gate still say that **sharing/revocation depth** and **output-taxonomy executable closure** remain bounded debt rather than closed law. See:
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`, lines 71-72 and 87-93
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`, lines 58-64

That means the next step should be **more executable proof**, not more prose-first policy.

---

## 2. Source-authority check

This evaluation used the active authority order defined in:
- `PROJECT_AUTHORITY.md`, lines 17-24 and 60-71
- `ACTIVE_SUBSTANCE_README.md`, lines 4-19

So the governing basis for this decision is:
1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`

Supporting but non-overriding material used for execution posture:
- `04_implementation_and_conformance/`
- `06_active_supporting_research/`

---

## 3. What the plan gets right

## 3.1 Correct constitutional placement

The plan correctly treats the feature as a **SharingGrant-governed Advisory capability**, not as farm-to-farm truth exposure.

That matches:
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`, lines 630-651
  - `SharingGrant` gives rights to see/retrieve/receive data/views/evidence/compiled outputs
  - farm-scoped truth remains farm-side
  - cross-farm/regional intelligence belongs in the Advisory Twin by default
  - revocation is prospective and does not erase truth history
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, lines 908-920
  - explicit sharing
  - scope-bounded visibility
  - farm/tenant boundary enforcement
  - governed pathways for regional/cross-farm intelligence
- `01_companion_artifacts/OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`, lines 113-128 and 132-169
  - sharing is explicit, scope-bounded, and distinct from truth authority
  - no implicit cross-farm sharing
  - regional intelligence should use opt-in plus aggregation/pseudonymization where possible

This part of the plan is sound.

## 3.2 Correct runtime family

The plan correctly places the feature in the **Advisory runtime**, not in Compliance or canonical state.

That matches:
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, lines 641-647
  - benchmark/explainability services are named as advisory/runtime services
- `01_companion_artifacts/OFARM_Advisory_Scenario_Workspace_and_Bridge_Note_v0_2.md`, lines 177-210
  - advisory results are not current state and must not silently bridge into harder truth

## 3.3 Correct evidence posture

The plan correctly assumes receipt scans are only the start of the chain.

That matches:
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, lines 324-336
  - capture is not commitment
  - scanner/document capture is document-first
  - OCR is helper only
  - review is required before governed commit
- `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`, lines 99-107
  - receipt scan captured is an `EvidenceEvent`
- `01_companion_artifacts/OFARM_Economic_Intelligence_Pack_Note_v0_2.md`, lines 126-142 and 167-180
  - economic values need evidence class, provenance, as-of, freshness, and direct-vs-derived posture
  - `ImportedFactExtract` is non-ledger by design

## 3.4 Correct anti-drift posture

The plan correctly avoids:
- new baseline-law changes
- new accepted RFCs
- new machine-contract promotion
- new passport families
- ERP/accounting drift

That matches the current economics stop rules and gate posture:
- `04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_acceptance_gate_report_v0_1.md`, lines 11-23 and 31-39
- `04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_day0_operator_checklist_v0_1.md`, lines 22-29
- `04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_economic_intelligence_promotion_gate_and_stop_rules_v0_1.md`, lines 11-20 and 24-39

---

## 4. Where the plan is still too broad or too vague

## 4.1 “Anonymized spend on a specific product” is still too broad for wave 1

The planning packet already warns against raw total spend as the default metric, but it still leaves too much room for wave-1 drift.

For wave 1, the following should be treated as **out of scope**:
- raw cohort total spend
- spend-per-hectare
- exact contributor counts
- min/max exposure to users
- percentile/distribution promises
- exact-product benchmarking by default

### Why

1. **Raw total spend is not meaningfully comparable across farms/tenants.**
2. **Exact-product cohorts create the highest disclosure risk.**
3. **Spend-per-hectare requires additional operational linkage and/or allocation basis**, which moves the seam closer to Scenario 2/3 economics rather than a minimal benchmark view.
4. **Min/max and exact counts create avoidable leakage pressure** even when names are hidden.

The economic pack note already says benchmark comparison is allowed **only with visible caution and basis disclosure** and that finer-grain economics must not be presented as observed truth without visible basis.
See `01_companion_artifacts/OFARM_Economic_Intelligence_Pack_Note_v0_2.md`, lines 203-212.

### Required narrowing

Wave 1 should be limited to:
- **price per normalized unit** for a governed product class or an exact normalized product only when exact normalization is reliable and cohort safety passes
- **quantity bands** where safe
- optionally **your position relative to cohort band**, not raw peer totals

## 4.2 The plan understates the query-shape problem

The packet says the current query subset may be enough. That is only **conditionally true**.

The current machine contract supports:
- `COUNT`
- `MIN`
- `MAX`
- `SUM`
- `AVG`
- result modes `SUMMARY_ROWS` and `VIEW_MODULE`

See `03_machine_contracts/schemas/query/OFARM_QuerySpecification_schema_v0_1.json`, lines 705-743 and 825-845.

But the accepted query RFC explicitly says v0.1 does **not** fully solve:
- future aggregate/group-by/windowing features
- full optimizer semantics

See `02_accepted_rfcs/OFARM_QuerySpecification_Schema_RFC_v0_1.md`, lines 193-200.

### Why this matters

A safe benchmark needs at least:
- minimum distinct contributors
- same-tenant multi-farm deduplication
- dominance checks
- safe fallback from exact product to broader class
- deterministic suppression behavior

Those are **not** cleanly expressible over raw invoice-line extracts with the current query surface unless a runtime quietly invents additional semantics.
That would violate the “no second query model” guardrail.

See:
- `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`, lines 53-67 and 109-118
- `01_companion_artifacts/OFARM_Advisory_Scenario_Workspace_and_Bridge_Note_v0_2.md`, lines 167-175 and 235-239

### Critical conclusion

The plan should no longer treat a benchmark-contribution object as optional.

A safe first wave needs an **explicit experimental contribution layer in `04`** so the current aggregate subset remains enough.


## 4.2a There is a bounded scope-model awkwardness, but not yet a blocker

The benchmark use case is cross-tenant/cross-farm by nature.
The current query schema does **not** expose `TENANT` or `DEPLOYMENT` as `QuerySpecification` scope types.
See `03_machine_contracts/schemas/query/OFARM_QuerySpecification_schema_v0_1.json`, lines 82-92.

By contrast, the authorization trace schema already recognizes broader runtime target scopes including `DEPLOYMENT` and `TENANT`.
See `03_machine_contracts/schemas/authority/OFARM_AuthorizationDecisionTrace_schema_v0_1.json`, lines 60-72.

### Why this matters

For a reusable benchmark product surface, a first-class cohort/deployment anchor might eventually become attractive.
But that would push the seam toward `02/03` contract changes, which are not justified yet.

### Required consequence

Wave 1 should avoid scope-model expansion by using one of these bounded patterns only:
- a saved query/view compiled with an explicit list of participating farm scopes
- or a benchmark-contribution layer whose own derivation already resolves cohort membership before query execution

If neither pattern works in practice, **that** would be the first credible trigger for a later `02/03` patch.

## 4.3 The plan leaves grant topology too open

The packet asks useful questions, but it does not fix the share path tightly enough.

For this capability, the smallest safe grant topology is:

1. **Contributor -> Benchmark Operator / Service Party**
   - explicit `SharingGrant`
   - purpose-bounded to cohort benchmarking
   - grants read/use of reviewed extract + normalization basis needed for contribution generation

2. **Benchmark Operator / Service -> Viewer**
   - explicit `SharingGrant`
   - grants only the benchmark view/report
   - grants `RECEIVE_READ_DATA` only
   - denies raw evidence and raw contribution rows

3. **Revocation**
   - contributor revocation blocks future contribution use and future recompute
   - already-issued frozen reports are governed by existing prospective revocation law

This stays within active authority law; no new constitutional authority family is needed.
See:
- `02_accepted_rfcs/OFARM_Authority_Policy_Model_RFC_v0_1.md`, lines 39-52, 70-107, 162-182, and 271-285
- `02_accepted_rfcs/OFARM_Authority_Action_Matrix_v0_1.md`, lines 26-28
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_runtime_sharing_boundary_access_records_v0_1.json`, scenario `share-06-cross-farm-advisor-no-share-deny`

## 4.4 The plan does not yet separate access control from disclosure control strongly enough

Existing authority machinery governs **who may access**.
It does **not** by itself solve whether the accessed view is disclosure-safe.

That distinction is already implicit in the baseline: sharing/access is explicit, but benchmark safety also needs suppression and anti-differencing rules.
The active authority set does **not** yet define those rules.

### Required consequence

The seam needs a separate deterministic **benchmark disclosure decision** layer in `04`.
This can be represented initially as fixture/result records rather than a promoted machine contract.

The good news is that the current authorization result contract already allows arbitrary uppercase reason codes and problem records, so benchmark-specific refusal/suppression codes do **not** require `03` patching yet.
See `03_machine_contracts/schemas/authority/OFARM_AuthorizationDecisionResult_schema_v0_1.json`, lines 123-176.

## 4.5 The plan is too optimistic about exact product identity from receipt-backed data

The active baseline gives a clean product-related anchor in `AppliedResource`, and the alignment register already expects external-profile reuse here.
See:
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`, line 81
- `01_companion_artifacts/OFARM_External_Standards_Integration_and_Interoperability_Policy_v0_1.md`, lines 117-130

But the plan still leaves too much ambiguity around exact product identity.

### Required consequence

Wave 1 should prefer this posture:
- use **reviewed line-item extracts** as raw basis
- add a separate **ProductNormalizationTrace** in `04`
- normalize to either:
  - exact governed product ref, or
  - governed broader product class
- fail clearly when normalization is ambiguous

Do **not** silently embed product normalization into the raw extract itself as if OCR text had become truth.

So the preferred implementation direction is:
- **Option B, not Option A**

That keeps raw-versus-interpreted discipline intact.

## 4.6 The plan is too early on companion-artifact drafting

The packet proposes a future companion-artifact policy note.
That is probably right **later**.
It is too early **now**.

### Why

The hostile review explicitly says sharing/revocation depth and output-taxonomy closure are still too prose-heavy and still need executable closure.
See:
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`, lines 71-72 and 87-93
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`, lines 60-64

So the next step should be:
- `06` research clarification
- `04` executable benchmark spike
- **then** a narrow `01` companion policy if the executable seam stabilizes

---

## 5. Required amendments to the plan

## A1. Replace the wave-1 capability statement

Replace the current first-wave capability with:

> A tenant/farm user may view a disclosure-controlled Advisory benchmark for a governed fertilizer or seed product class, or an exact normalized product only when normalization and cohort-safety rules pass, based on explicitly opted-in reviewed contribution artifacts derived from receipt-backed invoice-line extracts. The user never receives raw tenant rows or raw evidence through this capability.

## A2. Make raw total spend explicitly out of scope for wave 1

Add a hard boundary:
- no raw peer total-spend exposure in wave 1
- no spend-per-hectare in wave 1
- no exact contributor counts in wave 1
- no min/max exposure in wave 1
- no percentiles/distributions in wave 1

## A3. Make the two-leg share path mandatory

The plan should no longer leave the share topology open-ended.
It should require:
- contributor-to-operator share
- operator-to-viewer share
- no raw row or raw evidence exposure to viewers

## A4. Make experimental benchmark objects mandatory in `04`

The smallest controlled patch is:

1. `ProductNormalizationTrace` — experimental object in `04`
2. `BenchmarkContribution` — experimental object in `04`
3. benchmark disclosure decision records — experimental runtime outputs in `04`

### Why this is the smallest safe patch

A one-row-per-participant-per-product-per-window `BenchmarkContribution` object lets the current query aggregate subset remain enough:
- `COUNT` = contributor count
- `SUM` = cohort total of the contribution metric
- `MAX` = dominance testing
- `AVG` = average contribution metric

That avoids reopening group-by/distinct/window law in `02/03`.

### Required properties of `BenchmarkContribution`

It should be explicit that this object is:
- Advisory-only
- derived
- revocable for future use
- traceable to reviewed extracts + normalization trace + benchmark window
- not canonical truth
- not a ledger object
- not a hidden current-state store

## A5. Add a disclosure-control work package before any user-facing benchmark output

The disclosure-control package must define at least:
- minimum distinct contributors
- dominance threshold
- safe filter whitelist
- differencing guard
- fallback from exact product to broader class or refusal
- contributor-count display posture: hidden or banded, not exact by default

## A6. Change the pre-implementation outcome from `01 + 04` to `04`-only

The current review outcome should be:
- `06` research memo(s)
- `04` experimental contracts, fixtures, and hostile tests
- no new `01` artifact yet
- no `00/02/03` changes

A narrow `01` disclosure policy note may be drafted only after the `04` seam proves stable.

## A7. Narrow the pilot strategy

The plan should not start with a real-farm redacted pilot as the first executable proof.

Instead:
1. synthetic or semi-synthetic redacted multi-participant hostile dataset
2. executable disclosure/suppression fixtures
3. only then a bounded real-farm pilot packet if enough safe cohort size exists

This is necessary because a real pilot may not provide enough cohort size or variation to test suppression and differencing honestly.

## A8. Add currency/unit comparability refusal rules

Wave 1 should refuse when:
- units are not normalizable under the chosen product class
- currency basis is mixed without a governed FX posture
- packaging/treatment/formulation differences break comparability

The active external-standards posture already provides the right semantic anchors for this:
- QUDT for quantity/unit semantics
- UCUM for payload unit codes
- AIM / AGROVOC / EPPO as profile/code-binding aids where appropriate

See `01_companion_artifacts/OFARM_External_Standards_Integration_and_Interoperability_Policy_v0_1.md`, lines 117-130.

---

## 6. Revised implementation posture after critical evaluation

## 6.1 Affected files now

### Active baseline (`00_active_baseline/`)
No changes justified now.

### Accepted RFCs (`02_accepted_rfcs/`)
No changes justified now.

### Machine contracts (`03_machine_contracts/`)
No changes justified now.

### Active supporting research (`06_active_supporting_research/`)
Add:
- `OFARM_research_advisory_cohort_benchmark_capability_v0_1.md`
- `OFARM_research_advisory_cohort_benchmark_disclosure_controls_v0_1.md`
- `OFARM_research_advisory_cohort_benchmark_product_normalization_v0_1.md`

### Active supporting implementation/conformance (`04_implementation_and_conformance/`)
Add a bounded spike package, for example:
- `ofarm_advisory_cohort_benchmark_spike_v0_1/experimental_machine_contracts/`
- `ofarm_advisory_cohort_benchmark_spike_v0_1/fixtures/`
- `ofarm_advisory_cohort_benchmark_spike_v0_1/validation/`

### Companion artifacts (`01_companion_artifacts/`)
Defer for now.
Only revisit after `04` proof stabilizes.

## 6.2 Change classification

Current classification should be:
- **supporting research implication**
- **implementation/conformance implication**

Not yet justified:
- baseline law change
- new accepted RFC
- promoted machine contract

---

## 7. Revised go / narrow / stop decision matrix

## GO, with narrowing, only if all of the following are accepted now

1. Wave 1 is **not** “show me what others spent” in raw form.
2. Wave 1 is a **disclosure-controlled benchmark card/view**.
3. Exact product is conditional; product-class benchmark is the default fallback.
4. `BenchmarkContribution` and `ProductNormalizationTrace` are treated as required experimental `04` artifacts.
5. Pre-implementation remains `04`-only until executable proof exists.

## CUT BACK immediately if any of the following become true

1. The team insists on raw total-spend visibility as the main user outcome.
2. Exact-product normalization cannot be made deterministic enough.
3. The only workable design requires undeclared group-by/distinct/window semantics in the live query surface.
4. The viewer needs access to raw invoice-line rows for the benchmark to function.
5. A real pilot cannot satisfy safe cohort-size and suppression testing needs.

## STOP if either of these becomes true

1. The feature needs `00/02/03` changes just to get the first safe prototype running.
2. The feature drifts into procurement, AP/AR, ledger, or economic current-state semantics.

---

## 8. Bottom line

The planning packet is **good enough to continue**, but not good enough to execute unchanged.

The smallest controlled correction is:

1. keep the capability in the **Advisory Twin**
2. keep cross-tenant access **explicit-share only**
3. change the user outcome from **raw anonymized spend visibility** to **disclosure-controlled benchmark view**
4. require an experimental **ProductNormalizationTrace + BenchmarkContribution** layer in `04`
5. keep pre-implementation **`04`-only** until executable proof stabilizes
6. only then consider a narrow `01` companion-artifact policy note

That path respects the current active baseline, avoids reopening architecture, and closes the two real gaps without inventing new constitutional law prematurely.
