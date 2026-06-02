# OFARM pre-implementation strengthening pass for staple-crop scenario resilience v0.1

Date: 2026-04-14  
Status: pre-implementation strengthening packet  
Scope: convert the remaining scenario-derived weak points into controlled pre-implementation artifacts, directions, and acceptance obligations without reopening RC2.1 architecture

---

## 1. Executive judgment

The newest package is already much stronger than the earlier RC2.1 baseline snapshot. The correct move is still **not** to reopen architecture.

The scenario stress pass shows that the remaining weak points are now concentrated in five areas:

1. campaign realism for staple-crop operations
2. poor-but-real evidence handling and later evidence upgrade
3. high-consequence freshness tuning for storage, filing, and delivery flows
4. campaign-scale query and retrieval regression
5. deployment-produced gate/trace evidence for the hardest real-world seams

These are no longer architecture holes. They are **closure depth** problems.

This pass therefore keeps the patch small:
- **no Constitution rewrite**
- **no Platform rewrite**
- **no new top-level event family**
- **no new generic traceability ontology**
- **no new hidden truth layer**

Instead, it proposes:
- one small companion-artifact extension for evidence-quality handling
- one campaign-fixture library for staple crops
- one freshness/use-profile implementation spec
- one campaign-query regression spec
- one deployment-evidence obligations spec

That is enough to turn the remaining weak parts from “named concerns” into **executable implementation obligations**.

---

## 2. What is weak after the newest package inspection

### 2.1 No longer weak enough to justify architecture change

The newest package already made these areas materially stronger:
- lot continuity closure
- context snapshot grounding
- alias governance closure
- evidence sufficiency structure for high-consequence paths
- authority/action traces and pack-merge traces
- conformance depth across most constitutional seams

Those earlier debts should be treated as **closed enough for implementation direction**.

### 2.2 Still weak in a scenario-specific way

The real remaining risk is not “missing law”. It is that the package can still look stronger on paper than it will feel under ordinary staple-crop campaigns.

The highest-value weak points are:

#### A. Campaign realism is still thinner than single-seam conformance
The package now covers many seams well, but staple-crop reality is multi-step and multi-party. Partial replant, wet grain held before drying, sublot testing after bin splits, mixed organic/conventional handling, contractor late records, and post-filing correction are still not expressed as one coherent executable campaign family.

#### B. Evidence quality is structured for sufficiency, but not yet strongly enough for degraded everyday farm evidence
The package now has evidence-sufficiency structure, but it still does not explicitly grade the kinds of weak evidence that dominate real farming: ambiguous product IDs, free-text notes, OCR-derived labels, partial machine exports, late evidence, missing event timestamps, or conflict between human and machine records.

#### C. Freshness law is sound, but domain-grade use profiles are still thin
The package already has FRESH/STALE/INVALID and recompute/refuse rules. What it lacks is scenario-specific operational tuning for staple-crop campaigns such as wet-grain handling, grain drying, storage condition monitoring, buyer delivery, subsidy filings, and inspection dossiers.

#### D. Query law is strong, but campaign-scale retrieval regression is still too thin
The package does not yet force enough scenario-grade proof for questions like:
- what was in this bin at the time of the incident?
- which evidence supported the accepted executed consequence?
- which lot claim basis was in force before and after a reset?
- what changed across a field revision without changing field identity?

#### E. The last truly implementation-only debt is deployment-produced evidence
The newest package itself already says the remaining debt is concentrated in deployment-produced gate sequencing, projection trace-back, and live evidence for bridge promotion. That cannot be closed in prose alone, but it can be turned into a tight collection obligation before implementation starts.

---

## 3. Controlled patch set

## Patch 1 — Evidence-quality handling becomes explicit

### Affected active files
- `01_companion_artifacts/OFARM_Evidence_Sufficiency_and_Attestation_Policy_v0_1.md`
- `01_companion_artifacts/NEW: OFARM_Evidence_Quality_and_Promotion_Handling_Note_v0_1.md`
- `03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_1.json` → narrow `v0.2` extension during implementation
- new `OFARM_EvidenceSufficiencyCase_example_*` payloads for degraded-evidence scenarios
- fixture/result additions under `04_implementation_and_conformance/`

### Change type
Companion-artifact extension plus machine-contract and implementation/conformance implication.

### Smallest controlled patch
Do **not** change truth law, event families, or commit classes.

Add one companion note that standardizes how OFARM should assess weak-but-real evidence using the already accepted promotion and evidence-sufficiency structure.

The note should define five evaluation axes:
1. **source specificity** — exact identifier vs ambiguous/free-text reference
2. **capture integrity** — original/durable source vs transcription/OCR-only/memory-only
3. **chronology integrity** — exact event time vs bounded event time vs record-time only
4. **cross-source agreement** — human-only, machine-only, consistent, partial, conflicting
5. **late-arrival posture** — on-time, late before decision, late after frozen output, late after formal submission

The note should then define the allowed effects:
- weak evidence may support `note`, `observation assertion`, `hypothesis assertion`, `operation claim`, or `evidence record`
- weak evidence may **not** silently create an accepted executed intervention consequence or compliance fact
- stronger later evidence may strengthen a claim without changing earlier record time
- late evidence after a frozen output must create a new review/supersession path and a new frozen output version, not edit the prior one in place

### Why this is enough
This closes the specific real-farm failure mode where evidence exists but is poor quality. It avoids a much larger redesign and uses existing OFARM law.

### Risks if omitted
- implementers invent private quality ladders
- one runtime treats OCR text as enough while another does not
- late PPP or contractor evidence is handled by overwrite rather than supersession
- inspection/submission correction becomes inconsistent across deployments

### Acceptance conditions
This patch is only “done” when the package has explicit fixtures for:
- ambiguous PPP identifier upgraded later by label photo and invoice
- partial ISOXML task file plus manual top-up note
- late lab report arriving after a spray or storage decision
- post-submission evidence arrival creating a superseding package

---

## Patch 2 — Staple-crop campaign fixtures become first-class

### Affected active files
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_seed_set_v0_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`
- `04_implementation_and_conformance/NEW: OFARM_Staple_Crop_Campaign_Fixture_Library_v0_1.md`
- new fixture directories and result artifacts under `04_implementation_and_conformance/`

### Change type
Implementation/conformance implication.

### Smallest controlled patch
Do not add new constitutional objects.
Use the existing object families and machine contracts to build 12 executable staple-crop campaigns.

Minimum campaign set:
1. partial replant with overlap lineage
2. crop switch after failure with filing correction
3. variable-rate fertiliser with partial machine logs and manual correction
4. ambiguous PPP record with later evidence upgrade
5. wet grain hold → drying → storage → delivery
6. storage sanitation failure → insects/quality risk
7. harvest lot split → sublot test → partial merge → buyer rejection
8. organic/conventional shared equipment and storage segregation
9. spray-drift dispute across farms
10. contractor late reporting plus revocation boundary before promotion
11. post-filing late evidence and superseding submission
12. recipient-profile retrieval across buyer/certifier/farm roles

Each campaign must prove:
- event-family correctness
- commit/promotion discipline
- identity/lifecycle correctness
- freshness behavior
- authority separation
- pack interaction behavior where relevant
- output-family correctness
- query/retrieval correctness

### Why this is enough
The package already has good seam contracts. The missing strength is the stitching together of those seams into realistic campaigns.

### Risks if omitted
- implementations pass conformance while still failing ordinary farm operations
- lot and freshness logic looks correct in isolation but breaks in week-long campaigns
- multi-party flows pass unit tests and fail in filing or dispute conditions

### Acceptance conditions
This patch is only “done” when each campaign has:
- input payloads
- expected gate outcomes
- expected traces
- expected query results
- expected output-family result
- at least one negative case proving refusal or review-routing

---

## Patch 3 — Freshness becomes use-profiled for staple-crop campaigns

### Affected active files
- `04_implementation_and_conformance/NEW: OFARM_High_Consequence_Freshness_Profiles_for_Staple_Crop_Campaigns_v0_1.md`
- `03_machine_contracts/OFARM_MaterializationRequest_example_*` additions during implementation
- fixture/result additions under `04_implementation_and_conformance/`

### Change type
Implementation/conformance implication.

### Smallest controlled patch
Do not change freshness law.
Add use-profile guidance that binds existing freshness law to staple-crop campaign classes.

Required profiles:
1. establishment/replant decision profile
2. nutrient and PPP compliance profile
3. wet-grain and storage-condition profile
4. buyer delivery / quality claim profile
5. inspection/dossier/submission profile

For each, define:
- what counts as a materialization anchor
- what trigger families matter most
- when stale is still acceptable for exploratory use
- when stale becomes invalid for high consequence
- when a retained MaterializationSnapshot is mandatory

### Why this is enough
The law is already there. What is missing is a disciplined operational interpretation that prevents implementers from hard-coding arbitrary freshness shortcuts.

### Risks if omitted
- storage or delivery logic silently relies on old moisture/temperature state
- advisory freshness posture bleeds into compliance or attestation
- teams over-recompute or under-recompute with no common policy

### Acceptance conditions
This patch is only “done” when fixtures prove at least:
- a new drying event invalidates a prior delivery-quality state
- a field revision invalidates a subsidy submission state but not a historical advisory view
- a new lab result invalidates a prior dossier basis for attested use
- late evidence after a frozen output creates a new basis, not a hidden patch

---

## Patch 4 — Campaign-query regression becomes explicit

### Affected active files
- `04_implementation_and_conformance/NEW: OFARM_Campaign_Query_and_Retrieval_Regression_Spec_v0_1.md`
- new `QuerySpecification`/`QueryPlanIR` examples and results under `03_machine_contracts/` and `04_implementation_and_conformance/`

### Change type
Implementation/conformance implication.

### Smallest controlled patch
Do not change query law or public query posture.
Add a campaign-query regression spec using the existing canonical internal query model.

Minimum canonical query families:
1. `as_of_incident_scope_state`
2. `current_storage_contents`
3. `evidence_supporting_accepted_consequence`
4. `lot_claim_basis_before_after_reset`
5. `same_field_across_revision`
6. `recipient_specific_lot_view`
7. `late_evidence_supersession_chain`

Each query family must have:
- canonical meaning statement
- at least one valid query example
- at least one invalid or ambiguous example
- expected execution-target equivalence rule
- explicit trace-back obligation

### Why this is enough
OFARM’s query model is already formal. This patch forces scenario-grade retrieval proof without reopening query design.

### Risks if omitted
- query correctness is proven only on abstract toy shapes
- materialized/index-backed paths diverge from graph-backed truth in exactly the hard scenarios
- “what was true when” queries become deployment-specific folklore

### Acceptance conditions
This patch is only “done” when equivalent answers are proven across at least two execution targets for each required query family and when the negative cases fail clearly rather than degrade silently.

---

## Patch 5 — Deployment evidence obligations are fixed before implementation starts

### Affected active files
- `04_implementation_and_conformance/NEW: OFARM_Deployment_Evidence_Obligations_for_Hard_Scenarios_v0_1.md`
- later emitted telemetry/result artifacts from real implementations

### Change type
Implementation/conformance implication.

### Smallest controlled patch
Do not pretend this can be closed before code exists.
Instead, define the exact evidence that every implementation/pilot must emit.

Required record families:
1. enforcement-gate sequencing records
2. publication/output trace-back linkage records
3. materialization-use records for high-consequence paths
4. authority-decision emission records
5. offline-sync conflict and late-evidence reconciliation records
6. bridge-evidence intake records where same-standard surfaces are in scope

The spec should require stable identifiers, basis refs, context refs, output refs, actor refs, outcome codes, and redaction/sovereignty posture.

### Why this is enough
The newest package already says the remaining partial debt is deployment evidence, not missing architecture. This patch makes that debt measurable and non-negotiable.

### Risks if omitted
- pilots produce demos but not reusable evidence
- live bridge or partner-output decisions become non-reproducible
- partial deployment evidence gets mistaken for full closure

### Acceptance conditions
This patch is only “done” when the first implementation can emit these records as native outputs of ordinary flows rather than as one-off debugging artifacts.

---

## 4. What becomes strong now vs what remains implementation-collected

### Strong immediately after this strengthening pass
These areas can become strong **before implementation** because the gap is mainly specification and conformance design:
- evidence-quality handling
- campaign fixture design
- freshness use profiles
- campaign-query regression obligations
- deployment telemetry and trace-back evidence obligations

### Still implementation-collected by nature
These areas cannot become fully strong without running code and real pilot flows:
- emitted live gate-sequencing evidence
- emitted live projection/output trace-back evidence
- live same-standard bridge evidence and production approval
- real contractor/import/offline telemetry under revocation and late evidence

The important distinction is that after this pass these implementation-only gaps are **no longer vague**. They become explicit collection obligations.

---

## 5. What should not be added in this pass

Do not add any of the following unless implementation proves a real contradiction:
- a new top-level event family
- a generic constitutional `TraceObject`
- a new truth layer for storage state
- a public expert query language
- hidden output-side truth shortcuts
- hard-coded agronomic threshold constants inside core law

The staple-crop strengthening pass should stay disciplined.

---

## 6. Priority order

1. Patch 1 — evidence-quality handling
2. Patch 2 — staple-crop campaign fixtures
3. Patch 3 — freshness use profiles
4. Patch 4 — campaign-query regression
5. Patch 5 — deployment evidence obligations

That order keeps OFARM aligned with the active baseline and turns the weak parts into implementable obligations with the smallest controlled patch.

---

## 7. Deliverables in this packet

This packet includes:
- `OFARM_Evidence_Quality_and_Promotion_Handling_Note_v0_1.md`
- `OFARM_Staple_Crop_Campaign_Fixture_Library_v0_1.md`
- `OFARM_High_Consequence_Freshness_Profiles_for_Staple_Crop_Campaigns_v0_1.md`
- `OFARM_Campaign_Query_and_Retrieval_Regression_Spec_v0_1.md`
- `OFARM_Deployment_Evidence_Obligations_for_Hard_Scenarios_v0_1.md`
- `OFARM_post_strengthening_stress_test_prompt_v0_1.md`
- `OFARM_strengthening_action_matrix_2026-04-14.csv`
