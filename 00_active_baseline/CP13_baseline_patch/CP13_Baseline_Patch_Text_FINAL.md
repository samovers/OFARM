# CP13 Phase 4 — Baseline Patch Plan

Date: 2026-05-29  
Status: controlled baseline patch plan  
CP13 RFC basis: `02_accepted_rfcs/OFARM_Learning_Experimentation_and_Farm_Memory_RFC_v0_1.md` draft candidate  
Patch type: baseline addenda only; no full rewrites  
Machine-contract status: not drafted in this phase  
CP14/CP15 status: not started  
CP11/CP12 draft schema promotion: not performed

---

## 0. Phase 4 verdict

CP13 should proceed as a controlled baseline extension.

The patch should add a bounded learning, experimentation, causal-evidence, farm-memory, and seasonal-learning layer without changing OFARM's existing truth, authority, current-state, Advisory/Compliance, pack, query/output, CP11 charter, or CP12 mission-envelope law.

Core CP13 invariant:

```text
Learning output is not truth.
Experiment result is not automatic causal fact.
Farm memory is not hidden current state.
Agent memory is not farm memory.
Causal estimate is not compliance fact.
Model improvement is not deployment authority.
Mission or operation records may inform learning, but they do not become learning law by themselves.
```

The patch should be appended as controlled addenda. It should not rewrite the Constitution, Runtime architecture, Alignment Register structure, readiness framework, or hostile-review framework.

---

# 1. Patch plan summary

## 1.1 Affected baseline files

```text
00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md
00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md
00_active_baseline/OFARM_Alignment_Register_v0_13.md
00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md
00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md
```

## 1.2 Baseline patch posture

| File | Patch type | Baseline now? | Detail remains below baseline? |
|---|---|---:|---:|
| Constitution | Append CP13 model-law addendum | Yes | Yes, field/schema detail remains RFC/contracts/conformance |
| Platform Runtime | Append CP13 runtime-enforcement addendum | Yes | Yes, runtime topology remains implementation |
| Alignment Register | Add CP13 concept rows and alignment addendum | Yes | Yes, detailed schemas remain draft/non-default later |
| Readiness memo | Append CP13 readiness/non-claim addendum | Yes | Yes, stronger claims require evidence |
| Hostile review | Append CP13 hostile-review addendum | Yes | Yes, final hostile review after schemas/conformance may refine |

## 1.3 No-promotion rule

This Phase 4 patch must not:

```text
- promote CP11 draft/non-default schemas to current/default;
- promote CP12 draft/non-default schemas to current/default;
- create CP13 schemas;
- create CP14 or CP15 law;
- claim production autonomous self-improvement readiness;
- claim production agronomic-advice certification;
- claim farm-to-farm intelligence readiness;
- claim generated-software/model-deployment readiness.
```

---

# 2. File: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`

## 2.1 Patch C13-C-1 — Add CP13 baseline addendum

### Exact section to add or amend

Append after the CP12 baseline addendum:

```text
## CP13 Learning, Experimentation, and Farm Memory baseline addendum — 2026-05-29
```

### Proposed normative text

```text
## CP13 Learning, Experimentation, and Farm Memory baseline addendum — 2026-05-29

Status: controlled baseline patch candidate for `OFARM_Learning_Experimentation_and_Farm_Memory_RFC_v0_1.md`.

CP13 introduces a bounded learning, experimentation, causal-evidence, farm-memory, and seasonal-learning layer into OFARM model law.

CP13 does not replace the Constitution, create a second truth model, alter assertion/history-first authority, promote current-state materialisations into deeper truth, collapse the Advisory Twin and Compliance Twin, weaken CP11 charter gates, weaken CP12 cyber-physical mission gates, or make software agents hidden farm-memory governors.

The CP13 invariant is:

`Learning output is not truth. Experiment result is not automatic causal fact. Farm memory is not hidden current state. Agent memory is not farm memory. Causal estimate is not compliance fact. Model improvement is not deployment authority. Mission or operation records may inform learning, but they do not become learning law by themselves.`

A CP13 artifact may affect harder OFARM outcomes only through explicit authority, evidence, review, promotion, output, current-state, CP11, CP12, and later CP14/CP15 gates where applicable.

### CP13-C.1 Learning purpose and boundary

CP13 governs learning-sensitive uses where learning artifacts, experiment results, causal estimates, farm memory, seasonal summaries, or agent/model learning may materially affect recommendation, planning, claim, review, mission preparation, output, or future high-consequence reliance.

CP13 applies to crop-farming OFARM contexts already within the active baseline scope. It does not expand OFARM into livestock-specific learning, animal-welfare learning, herd/flock learning, feeding, treatment, movement, or animal-health learning law.

CP13 is not generic AI memory, farm-to-farm intelligence, federated learning, model deployment governance, generated-software delivery governance, or production autonomous self-improvement readiness.

### CP13-C.2 CP13 core concepts

The following CP13 concepts are baseline-recognised OFARM-governed concepts and must be represented in the Alignment Register before they are treated as constitutional core:

- `LearningScope`;
- `LearningHypothesis`;
- `ExperimentProtocol`;
- `TrialDesign`;
- `ExperimentalUnit`;
- `TreatmentArm`;
- `ControlCondition`;
- `RandomizationPlan`;
- `BlockingFactor`;
- `OutcomeMeasureSpec`;
- `OutcomeObservationSet`;
- `LearningEvidenceBundle`;
- `LearningEvaluationTrace`;
- `CausalEstimate`;
- `LearningPromotionDecision`;
- `FarmMemoryEntry`;
- `FarmMemoryInvalidationRule`;
- `FarmMemoryRetrievalQualification`;
- `SeasonalLearningSummary`;
- `LearningOutputQualification`;
- `ExperimentRollbackTrigger`;
- `ExperimentException`.

These concepts may be detailed by accepted RFCs, companion artifacts, draft/non-default machine contracts, and conformance fixtures. They may not be introduced silently through an app, pack, adapter, AI memory, vector store, dashboard, world-model state, or external model registry.

### CP13-C.3 Learning artifact family and truth boundary

CP13 learning artifacts are not alternate truth stores.

A `LearningHypothesis` is a testable proposition. It is not fact.

An `ExperimentProtocol` or `TrialDesign` governs learning design. It is not authority to perform a field operation, apply an input, dispatch a robot or machine, approve a CP11 charter exception, publish a claim, share data cross-farm, or deploy a model/software change.

An `OutcomeObservationSet` is grouped evidence input. It is not a causal conclusion by itself.

A `CausalEstimate` is a qualified estimate of an effect under declared scope, method, evidence, assumptions, uncertainty, and limitations. It is not causal truth, Compliance Twin fact, claim basis, or operational authority by itself.

A `FarmMemoryEntry` is governed, scoped, evidence-linked, retrieval-qualified, and invalidation-aware local farm memory. It is not hidden current state, hidden canonical truth, hidden governance, or agent memory.

A `SeasonalLearningSummary` is a season-bounded summary. It is not a blanket truth update or automatic current-state mutation.

### CP13-C.4 Learning scope and locality

High-consequence CP13 artifacts must declare a `LearningScope` or explicit inherited scope. A learning scope must identify the spatial, temporal, biological, operational, equipment, evidence, and reuse boundary within which the learning artifact may be interpreted.

Default posture:

`CP13 learning is local/farm-scoped unless CP14 explicitly governs cross-farm use.`

A farm memory entry, causal estimate, seasonal learning summary, or learning-derived recommendation must not be reused outside its declared `LearningScope` without retrieval qualification, scope-expansion review, or later CP14-governed exchange law.

### CP13-C.5 Experimentation and non-authorisation

An `ExperimentProtocol`, `TrialDesign`, `RiskBudget`, or `RegretBudget` does not authorise operations or missions by itself.

Operations still require ordinary OFARM operation/intervention law. Cyber-physical missions still require CP12. Sustainability-sensitive trial actions still require CP11. Cross-farm learning requires CP14. Model/software deployment requires CP15.

Where an experiment or trial would materially affect soil, water, biodiversity, chemical/input use, safety, mission authority, output claims, data sharing, or high-consequence decisions, applicable CP11 and CP12 gates remain in force.

### CP13-C.6 Outcome measures, evidence, and causal uncertainty

Where a learning output claims experimental or causal support, it must disclose whether outcome measures were predeclared, amended, added post hoc, excluded, substituted, or missing.

A CP13 `LearningEvidenceBundle` must preserve evidence provenance, quality, missingness, bias, stale/invalid status, current-state reliance where applicable, CP11/CP12 dependencies where material, and uncertainty.

A `LearningEvaluationTrace` must record the scope, design, assumptions, evidence basis, outcome-measure posture, missingness, comparison basis, uncertainty, review posture, blocked/review-required conditions, and output disposition used to evaluate a learning result.

A `CausalEstimate` must expose effect estimate, uncertainty, comparison basis, method, assumptions, scope, validity horizon, limitations, and prohibited uses. Weak, observational, modelled, post-hoc, or underpowered evidence must not be represented as strong experimental support.

### CP13-C.7 Learning promotion and farm memory

A learning result may become a `FarmMemoryEntry` only through a governed `LearningPromotionDecision`.

A `LearningPromotionDecision` may decide, at minimum:

- promote to farm memory;
- keep advisory-only;
- require more evidence;
- require review;
- reject;
- supersede;
- invalidate;
- restrict reuse;
- defer to CP14 or CP15 where cross-farm exchange or deployment is involved.

A `FarmMemoryEntry` must declare evidence basis, scope, validity horizon, retrieval qualification, invalidation rules, confidence/uncertainty posture, and prohibited uses.

Farm memory must not update current state, create Compliance Twin fact, create claim basis, or authorise mission/operation by itself.

### CP13-C.8 Farm memory invalidation and retrieval

A `FarmMemoryInvalidationRule` must identify conditions that cause a farm memory entry to expire, downgrade, require review, or be invalidated.

A `FarmMemoryRetrievalQualification` is required when farm memory is retrieved for learning-sensitive or high-consequence use. It must disclose scope match, freshness, evidence strength, uncertainty, limitations, current applicability, and prohibited uses.

A retrieved farm memory entry may inform recommendations, planning, review packages, BridgeCandidates, or advisory reasoning. It may not silently act as hidden current state, hidden evidence sufficiency, hidden claim basis, hidden CP11 charter pass, hidden CP12 mission precondition, or hidden authority.

### CP13-C.9 Agent memory, training data, and model improvement boundary

Agent memory, model context, vector-store memory, prompt history, tool-call history, model weights, embeddings, and generated summaries are not OFARM farm memory.

A software agent may propose a learning hypothesis, prepare an experiment protocol draft, summarise outcome observations, propose a causal estimate, request evidence, prepare a learning evaluation trace candidate, or propose a farm-memory entry only within its authority envelope.

A software agent may not by default approve experiments, promote learning to farm memory, expand learning scope, approve cross-farm learning, deploy model/software changes, or create Compliance Twin facts.

A model improvement, prompt change, workflow change, adapter change, generated code artifact, or deployment candidate is not authorised by CP13. Deployment governance belongs to CP15.

### CP13-C.10 CP11 and CP12 integration

CP11 remains governing for sustainability-sensitive learning, experimentation, claims, charter evaluations, risk/regret budgets, exceptions, and output qualification.

CP12 remains governing for cyber-physical mission preparation, dispatch, command, telemetry, receipt, verification, incidents, and mission outputs.

CP12 mission telemetry, execution receipts, mission verification, near-miss records, and physical-safety incident records may serve as learning evidence candidates. They do not become learning conclusions, causal estimates, farm memory, or Compliance Twin facts merely by existing.

### CP13-C.11 Learning output qualification

A learning-sensitive output must carry a `LearningOutputQualification` where it may affect recommendation, planning, claim, review, mission preparation, CP11 charter evaluation, CP12 mission preparation, publication, export, or future high-consequence reliance.

A learning output must expose, where material:

- artifact type and lifecycle posture;
- scope;
- evidence strength;
- outcome-measure posture;
- causal strength;
- uncertainty;
- missingness;
- advisory/compliance posture;
- farm-memory promotion posture;
- CP11/CP12 dependencies;
- allowed uses;
- prohibited uses;
- required review or blocked-use reasons.

A learning output must not be represented as claim-ready, compliance-ready, mission-ready, deployment-ready, or cross-farm-shareable unless the applicable OFARM gates have been satisfied.

### CP13-C.12 Pack/profile interaction

Packs and profiles may specialise learning policy, experiment policy, outcome-measure rules, farm-memory retrieval/invalidation rules, learning-output qualification, and local-method profiles only through declared CP13 learning surface families and merge modes.

Learning pack/profile merge must fail closed where a conflict could weaken evidence requirements, hide uncertainty, loosen promotion rules, expand scope, alter invalidation posture, allow unsupported causal claims, bypass CP11/CP12 gates, or create hidden cross-farm/deployment authority.

### CP13-C.13 Authority and human-governed defaults

The following CP13 action classes are human-governed or human-approval-required by default unless a later active RFC explicitly relaxes posture for a bounded lower-risk class:

- approving an experiment protocol where it materially affects operations, CP11-sensitive decisions, CP12 mission preparation, or high-consequence outputs;
- approving learning promotion to farm memory;
- expanding a farm memory entry beyond its original learning scope;
- overriding a farm memory invalidation rule;
- approving a causal estimate for high-consequence use;
- approving a seasonal learning summary for publication, claim support, or external disclosure;
- approving cross-farm learning use, which remains CP14 territory;
- approving model/software deployment based on learning, which remains CP15 territory.

A software agent may support these workflows only within explicit authority and trace boundaries.

### CP13-C.14 Explicit deferrals

CP13 does not define farm-to-farm intelligence, federated learning, cross-farm benchmark exchange, regional alerts, derivative model-use policy, aggregation-floor rules, re-identification-risk handling, or cross-farm model contribution law. Those belong to CP14.

CP13 does not define generated-software delivery, model deployment, adapter generation, rollout, canary promotion, rollback, SBOM, build provenance, model-card governance, or deployment promotion. Those belong to CP15.

CP13 does not expand OFARM into livestock-specific learning, animal-welfare learning, herd/flock learning, feeding, treatment, movement, or animal-health learning law.

CP13 does not create production autonomous self-improvement readiness or production agronomic-advice certification.

### CP13-C.15 Non-claims

CP13 does not claim production autonomous self-improvement readiness, production agronomic advice certification, farm-to-farm intelligence readiness, federated learning readiness, regional alert readiness, model deployment readiness, generated-software readiness, CP14 readiness, CP15 readiness, legal advice, insurance advice, certification advice, or livestock learning readiness.
```

### Reason for the change

The active baseline now has CP11 sustainability governance and CP12 cyber-physical mission-envelope law. CP13 is the next missing constitutional layer because the platform can now govern charter-sensitive recommendations and physical missions, but it still lacks governed learning, experimentation, causal-evidence, farm-memory, and learning-promotion law.

### Interaction with existing law

This patch preserves:

```text
- assertion/history-first truth;
- current-state materialisation;
- Advisory/Compliance Twin separation;
- authority default-deny;
- pack law;
- output qualification;
- agent actorship and trace law;
- CP11 charter gates;
- CP12 mission gates.
```

It adds learning-specific boundaries and does not create operational, mission, cross-farm, or deployment authority.

### Risk of contradiction

Medium if `FarmMemoryEntry` is later implemented as hidden current state or if `CausalEstimate` is treated as accepted causal truth. Low if the no-hidden-truth and promotion-decision rules are preserved.

### Baseline law now or RFC law?

The invariant, concept recognition, authority boundary, output boundary, CP11/CP12 integration, and non-claims belong in baseline law.

Detailed field requirements, schemas, fixture logic, and examples remain RFC, companion artifact, draft/non-default machine-contract, and conformance material.

### Migration note

Existing local-knowledge, narrative observation, local memory, planned-intervention, world-model, and agent-memory material should not be reclassified automatically as CP13 farm memory. It remains under its existing category until a CP13 mapping, review, or promotion path explicitly applies.

### Conformance implication

CP13 conformance must prove at minimum:

```text
- learning artifacts do not create truth;
- experiment protocols do not authorise operations or missions;
- causal estimates do not create compliance facts;
- farm memory is not current state;
- agent memory is not farm memory;
- learning promotion requires governance;
- out-of-scope retrieval is blocked or qualified;
- CP11/CP12 gates are preserved where material;
- CP14/CP15 boundaries are not crossed.
```

---

## 2.2 Patch C13-C-2 — Amend artifact-family list by addendum reference only

### Exact section to add or amend

Do not rewrite `### 5.2 Artifact families`. Add the following sentence inside the CP13 baseline addendum after `CP13-C.2 CP13 core concepts`:

```text
The CP13 learning artifact family is a governed extension of OFARM knowledge, evidence, decision/governance, and output artifact families. It does not create a generic memory bucket or a new truth family.
```

### Proposed normative text

```text
The CP13 learning artifact family is a governed extension of OFARM knowledge, evidence, decision/governance, and output artifact families. It does not create a generic memory bucket or a new truth family.
```

### Reason

Avoids a broad rewrite of artifact-family law while making the family placement explicit.

### Interaction with existing law

It preserves existing artifact taxonomy and prevents a generic `LearningOutput` or `AgentMemory` truth bucket.

### Risk of contradiction

Low.

### Baseline law now or RFC law?

Baseline sentence only. Full taxonomy remains RFC law.

### Migration note

Existing `LocalMemoryRule` or agent memory does not automatically become `FarmMemoryEntry`.

### Conformance implication

Conformance must reject generic agent-memory or vector-memory artifacts being accepted as farm memory without CP13 promotion.

---

## 2.3 Patch C13-C-3 — Add learning-specific pack surface families by addendum

### Exact section to add or amend

Do not edit the original pack law tables in place. Add within `CP13-C.12 Pack/profile interaction`:

```text
CP13 learning surface families include, at minimum:

- LEARNING_POLICY;
- EXPERIMENT_PROTOCOL_POLICY;
- TRIAL_DESIGN_POLICY;
- OUTCOME_MEASURE_POLICY;
- LEARNING_EVIDENCE_POLICY;
- CAUSAL_ESTIMATE_POLICY;
- LEARNING_PROMOTION_POLICY;
- FARM_MEMORY_RETRIEVAL_POLICY;
- FARM_MEMORY_INVALIDATION_POLICY;
- LEARNING_OUTPUT_QUALIFICATION_POLICY;
- LEARNING_EXCEPTION_POLICY.
```

### Proposed normative text

```text
CP13 learning surface families include, at minimum:

- `LEARNING_POLICY`;
- `EXPERIMENT_PROTOCOL_POLICY`;
- `TRIAL_DESIGN_POLICY`;
- `OUTCOME_MEASURE_POLICY`;
- `LEARNING_EVIDENCE_POLICY`;
- `CAUSAL_ESTIMATE_POLICY`;
- `LEARNING_PROMOTION_POLICY`;
- `FARM_MEMORY_RETRIEVAL_POLICY`;
- `FARM_MEMORY_INVALIDATION_POLICY`;
- `LEARNING_OUTPUT_QUALIFICATION_POLICY`;
- `LEARNING_EXCEPTION_POLICY`.

Where a learning surface could weaken evidence, loosen promotion, expand reuse scope, hide uncertainty, weaken invalidation, bypass CP11/CP12, or create hidden CP14/CP15 authority, merge must fail closed or require explicit governance.
```

### Reason

CP13 will need pack/profile specialisation for local learning and experiment policy. The baseline should name the surface families but leave detailed merge modes to RFC and pack addenda.

### Interaction with existing law

Uses existing pack-surface law. Does not change core merge modes.

### Risk of contradiction

Medium if pack surfaces later allow scope expansion or evidence downgrades by default. Mitigate with fail-closed posture and conformance.

### Baseline law now or RFC law?

Surface-family recognition belongs in baseline. Detailed merge policy remains RFC/addendum.

### Migration note

Existing packs that contain learning guidance should be treated as touching undeclared learning surfaces until mapped.

### Conformance implication

Add fixtures for stricter learning policy merge, conflicting outcome-measure policy hard fail, and memory-retrieval policy conflict.

---

## 2.4 Patch C13-C-4 — Add CP13 authority action classes by addendum

### Exact section to add or amend

Do not rewrite `### 7.10 AuthorityActionClass`. Add under `CP13-C.13 Authority and human-governed defaults`:

```text
CP13 recognises learning-sensitive authority actions...
```

### Proposed normative text

```text
CP13 recognises the following learning-sensitive authority action classes:

- `LEARNING_PROPOSE_HYPOTHESIS`;
- `LEARNING_APPROVE_EXPERIMENT_PROTOCOL`;
- `LEARNING_AMEND_EXPERIMENT_PROTOCOL`;
- `LEARNING_APPROVE_TRIAL_DESIGN`;
- `LEARNING_DEFINE_OUTCOME_MEASURE`;
- `LEARNING_AMEND_OUTCOME_MEASURE`;
- `LEARNING_RECORD_OUTCOME_OBSERVATION_SET`;
- `LEARNING_PRODUCE_CAUSAL_ESTIMATE`;
- `LEARNING_APPROVE_CAUSAL_ESTIMATE_FOR_HIGH_CONSEQUENCE_USE`;
- `LEARNING_PROMOTE_TO_FARM_MEMORY`;
- `LEARNING_RETRIEVE_FARM_MEMORY_FOR_USE`;
- `LEARNING_EXPAND_SCOPE`;
- `LEARNING_INVALIDATE_FARM_MEMORY`;
- `LEARNING_APPROVE_SEASONAL_SUMMARY`;
- `LEARNING_APPROVE_OUTPUT_FOR_PUBLICATION`;
- `LEARNING_APPROVE_EXPERIMENT_EXCEPTION`;
- `LEARNING_APPROVE_ROLLBACK_TRIGGER`;
- `LEARNING_APPROVE_CROSS_FARM_USE`;
- `LEARNING_APPROVE_MODEL_OR_SOFTWARE_DEPLOYMENT_USE`.

`LEARNING_APPROVE_CROSS_FARM_USE` is a CP14 boundary action and must not authorise actual cross-farm exchange under CP13 alone.

`LEARNING_APPROVE_MODEL_OR_SOFTWARE_DEPLOYMENT_USE` is a CP15 boundary action and must not authorise deployment under CP13 alone.

High-consequence learning actions are human-governed or human-approval-required by default. Software agents may prepare, recommend, analyse, request evidence, and draft traces only under explicit authority; they may not by default approve protocols, promote farm memory, expand scope, approve cross-farm use, or approve deployment.
```

### Reason

Without explicit action classes, agents or workflows could become hidden learning governors.

### Interaction with existing law

Extends existing AuthorityActionClass/default-deny model. Does not replace authority law.

### Risk of contradiction

Low if defaults remain human-governed and CP14/CP15 boundary actions are non-authorising in CP13.

### Baseline law now or RFC law?

The action-class recognition belongs in baseline. Detailed authority matrix entries belong in CP13 RFC/addenda.

### Migration note

Existing grants do not automatically include CP13 learning authority.

### Conformance implication

Add fixtures proving agents cannot promote farm memory, approve protocol, approve cross-farm learning, or approve deployment by tool success.

---

# 3. File: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`

## 3.1 Patch C13-P-1 — Add CP13 runtime-enforcement addendum

### Exact section to add or amend

Append after the CP12 runtime-enforcement addendum:

```text
## CP13 Learning, Experimentation, and Farm Memory runtime-enforcement addendum — 2026-05-29
```

### Proposed normative text

```text
## CP13 Learning, Experimentation, and Farm Memory runtime-enforcement addendum — 2026-05-29

Status: controlled runtime patch candidate for `OFARM_Learning_Experimentation_and_Farm_Memory_RFC_v0_1.md`.

CP13 adds a runtime learning-governance gate for learning-sensitive use. It does not add autonomous self-improvement, farm-to-farm intelligence, model/software deployment authority, or production agronomic-advice certification.

### CP13-P.1 Learning-sensitive runtime surface

A runtime path is learning-sensitive when learning artifacts, experiment results, causal estimates, farm memory, seasonal summaries, agent/model learning, or learning-derived recommendations may materially affect recommendation, planning, review, claim, mission preparation, output, publication, export, or future high-consequence reliance.

Learning-sensitive paths must not write directly to canonical truth, current-state materialisation, Compliance Twin fact, mission authority, claim basis, or deployment authority.

### CP13-P.2 Learning governance gate

For learning-sensitive use, the platform must be able to resolve the applicable `LearningScope` and determine whether the use involves:

- hypothesis creation;
- experiment protocol or trial-design creation;
- outcome-measure definition;
- outcome observation grouping;
- evidence bundling;
- causal estimation;
- learning evaluation;
- learning promotion;
- farm-memory entry creation;
- farm-memory retrieval;
- seasonal learning summary;
- learning output;
- CP11 risk/regret budget use;
- CP11 charter-sensitive learning use;
- CP12 mission/operation evidence use;
- CP14 or CP15 boundary crossing.

The gate must emit or link a `LearningEvaluationTrace` where the outcome affects promotion, farm-memory creation, retrieval, high-consequence recommendation, output, review, claim support, CP11 charter-sensitive use, CP12 mission preparation, publication, export, or later CP14/CP15 handoff.

### CP13-P.3 Experiment and protocol non-authorisation

Runtime acceptance of an `ExperimentProtocol`, `TrialDesign`, `RiskBudget`, or `RegretBudget` must not by itself create operation authority, intervention execution truth, CP12 mission dispatch authority, CP11 charter exception, output publication approval, cross-farm sharing approval, or model/software deployment authority.

If the experiment requires a field operation, input application, physical mission, charter-sensitive action, data disclosure, or model/software deployment, the relevant OFARM authority path must be executed separately.

### CP13-P.4 Learning evidence and causal-estimate gate

A runtime path that produces a `CausalEstimate`, `LearningPromotionDecision`, `FarmMemoryEntry`, `SeasonalLearningSummary`, or high-consequence `LearningOutputQualification` must preserve:

- evidence provenance;
- learning scope;
- design and comparison basis;
- outcome-measure posture;
- missingness and bias posture;
- uncertainty;
- current-state reliance where applicable;
- CP11 and CP12 dependencies where material;
- review and promotion posture;
- allowed and prohibited use.

Weak, post-hoc, observational, modelled, or underpowered evidence must not be upgraded to strong causal or experimental support by runtime presentation.

### CP13-P.5 Farm-memory gate

A `FarmMemoryEntry` may be created only through a governed `LearningPromotionDecision` or another later accepted CP13 path. It must carry scope, evidence basis, validity horizon, retrieval qualification, invalidation posture, and prohibited uses.

Farm memory retrieval for learning-sensitive or high-consequence use must produce or link a `FarmMemoryRetrievalQualification`.

Farm memory must not be used as hidden current state, hidden evidence sufficiency, hidden CP11 charter pass, hidden CP12 mission precondition, hidden claim basis, hidden Compliance Twin fact, or hidden authority.

### CP13-P.6 Agent memory and model-learning boundary

Agent memory, vector memory, prompt history, tool-call history, model weights, embeddings, cached summaries, and model-improvement artifacts are not OFARM farm memory.

Software agents may propose learning artifacts, produce analysis, request evidence, draft traces, and recommend promotion only within explicit authority. They may not approve learning promotion, scope expansion, cross-farm use, or model/software deployment by default.

### CP13-P.7 CP11 and CP12 coupling

Where learning-sensitive use materially depends on CP11 charter state, sustainability constraints/objectives, risk/regret budgets, sustainability claims, charter exceptions, or charter breaches, the runtime must preserve CP11 gates and qualifications.

Where learning-sensitive use materially depends on CP12 mission plan, preflight, dispatch, command, telemetry, receipt, verification, abort, near-miss, or physical-safety incident records, the runtime must preserve CP12 stage separation and truth boundaries.

A CP12 mission verification may serve as learning evidence candidate. It does not create learning truth, causal fact, farm memory, or Compliance Twin fact by itself.

### CP13-P.8 Learning output gate

A learning-sensitive output must carry a `LearningOutputQualification` where it may affect recommendation, planning, review, CP11 charter evaluation, CP12 mission preparation, claim support, publication, export, or future high-consequence reliance.

The runtime must prevent learning outputs from being used as truth, claim basis, mission authority, compliance fact, cross-farm shareable intelligence, or deployment authority unless separate OFARM gates explicitly allow the harder use.

### CP13-P.9 Runtime non-claims

Runtime support for CP13 remains implementation-directed with bounded debt until CP13 machine contracts, conformance fixtures, hostile review, implementation evidence, and steward validation exist.

CP13 runtime support does not claim production autonomous self-improvement readiness, production agronomic-advice certification, farm-to-farm intelligence readiness, federated learning readiness, regional alert readiness, model deployment readiness, generated-software readiness, CP14 readiness, or CP15 readiness.
```

### Reason for the change

The Platform Runtime needs explicit enforcement points for learning-sensitive paths. Otherwise CP13 learning artifacts could become hidden truth, farm memory could become hidden current state, or agent memory could become de facto farm memory.

### Interaction with existing law

This is an additive runtime-enforcement layer. It uses existing enforcement concepts: authority, evidence, current-state, output qualification, agent run traces, CP11 gates, and CP12 mission boundaries.

### Risk of contradiction

Medium if runtime implementers treat learning retrieval as a cache read rather than governed retrieval. Low if retrieval qualification and promotion gates are enforced.

### Baseline law now or RFC law?

Runtime gate and non-bypass principles belong in baseline runtime law. Detailed service APIs, schemas, runners, storage, and algorithms remain RFC/implementation/conformance.

### Migration note

Existing world-model, agent memory, local observations, or local memory rules should be surfaced as existing categories until CP13 promotion maps them.

### Conformance implication

Conformance should include runtime fixtures proving that:

```text
- experiment protocols do not dispatch missions;
- farm memory cannot be used outside scope without qualification;
- causal estimates cannot create Compliance Twin facts;
- agent memory cannot be loaded as FarmMemoryEntry;
- CP12 telemetry cannot create farm memory without promotion;
- CP11 risk/regret budgets do not authorise experiments by themselves.
```

---

# 4. File: `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

## 4.1 Patch C13-A-1 — Add CP13 concept rows

### Exact section to add or amend

Append after the CP12 alignment update section:

```text
## CP13 Learning, Experimentation, and Farm Memory alignment addendum — 2026-05-29
```

### Proposed normative text

```text
## CP13 Learning, Experimentation, and Farm Memory alignment addendum — 2026-05-29

Status: controlled alignment patch candidate for CP13.

### CP13 concept rows to add

| Concept | Domain | Alignment class | External alignment | OFARM naming | Reason |
|---|---|---|---|---|---|
| LearningScope | Learning / Governance / Context | OFARM_OWNED | Experiment/scientific context models as anchors only | OFARM uses `LearningScope` | OFARM needs explicit scope for farm-local learning reuse and high-consequence learning outputs. |
| LearningHypothesis | Learning / Advisory | OFARM_OWNED | Scientific hypothesis models as anchors only | OFARM uses `LearningHypothesis` | OFARM needs testable propositions without treating them as facts. |
| ExperimentProtocol | Learning / Governance | OFARM_OWNED | Research protocol models as anchors only | OFARM uses `ExperimentProtocol` | OFARM needs governed experiment design without authorising operations or missions. |
| TrialDesign | Learning / Evidence | OFARM_OWNED | Agronomic trial-design standards as anchors only | OFARM uses `TrialDesign` | OFARM needs trial structure, controls, treatments, and outcome posture for learning claims. |
| ExperimentalUnit | Learning / Evidence | OFARM_OWNED | Agronomic/statistical trial concepts as anchors only | OFARM uses `ExperimentalUnit` | OFARM needs explicit units of assignment/comparison. |
| TreatmentArm | Learning / Evidence | OFARM_OWNED | Agronomic/statistical trial concepts as anchors only | OFARM uses `TreatmentArm` | OFARM needs to represent planned treatment differences without treating them as executed interventions. |
| ControlCondition | Learning / Evidence | OFARM_OWNED | Trial/comparison concepts as anchors only | OFARM uses `ControlCondition` | OFARM needs explicit baseline/comparison conditions for causal interpretation. |
| RandomizationPlan | Learning / Evidence | OFARM_OWNED | Statistical randomisation concepts as anchors only | OFARM uses `RandomizationPlan` | OFARM needs to distinguish randomised, blocked, observational, historical, matched, and modelled comparisons. |
| BlockingFactor | Learning / Evidence | OFARM_OWNED | Statistical blocking concepts as anchors only | OFARM uses `BlockingFactor` | OFARM needs to expose design factors affecting causal interpretation. |
| OutcomeMeasureSpec | Learning / Evidence | OFARM_OWNED | Measurement/specification concepts as anchors only | OFARM uses `OutcomeMeasureSpec` | OFARM needs predeclared outcome measures and outcome-hacking prevention. |
| OutcomeObservationSet | Learning / Evidence | OFARM_OWNED | Observation-set concepts as anchors only | OFARM uses `OutcomeObservationSet` | OFARM needs grouped outcome evidence without treating it as causal conclusion. |
| LearningEvidenceBundle | Learning / Evidence | OFARM_OWNED | PROV-O/evidence models as anchors only | OFARM uses `LearningEvidenceBundle` | OFARM needs learning-specific evidence bundles with provenance, missingness, bias, and uncertainty. |
| LearningEvaluationTrace | Learning / Traceability | OFARM_OWNED | PROV-O trace concepts as anchors only | OFARM uses `LearningEvaluationTrace` | OFARM needs traceability for how learning evidence becomes conclusions, promotion decisions, or qualified outputs. |
| CausalEstimate | Learning / Advisory / Evidence | OFARM_OWNED | Statistical/causal estimate concepts as anchors only | OFARM uses `CausalEstimate` | OFARM needs qualified effect estimates that are not truth or compliance facts by themselves. |
| LearningPromotionDecision | Learning / Governance | OFARM_OWNED | Governance/review concepts as anchors only | OFARM uses `LearningPromotionDecision` | OFARM needs governed promotion into farm memory or rejection/downgrade/invalidation. |
| FarmMemoryEntry | Learning / Local Knowledge | OFARM_OWNED | Local-knowledge concepts as anchors only | OFARM uses `FarmMemoryEntry` | OFARM needs scoped, governed farm-specific memory that is not hidden current state. |
| FarmMemoryInvalidationRule | Learning / Governance | OFARM_OWNED | Validity/invalidation concepts as anchors only | OFARM uses `FarmMemoryInvalidationRule` | OFARM needs memory expiry, downgrade, and invalidation. |
| FarmMemoryRetrievalQualification | Learning / Output / Runtime | OFARM_OWNED | Result-qualification concepts as anchors only | OFARM uses `FarmMemoryRetrievalQualification` | OFARM needs qualified retrieval so memory cannot be used outside scope silently. |
| SeasonalLearningSummary | Learning / Output | OFARM_OWNED | Seasonal reporting concepts as anchors only | OFARM uses `SeasonalLearningSummary` | OFARM needs bounded seasonal learning summaries that do not become truth updates. |
| LearningOutputQualification | Learning / Output | OFARM_OWNED | Result-qualification concepts as anchors only | OFARM uses `LearningOutputQualification` | OFARM needs allowed/prohibited-use qualification for learning outputs. |
| ExperimentRollbackTrigger | Learning / Safety / Governance | OFARM_OWNED | Safety/rollback concepts as anchors only | OFARM uses `ExperimentRollbackTrigger` | OFARM needs bounded conditions for stopping, downgrading, or reviewing experiments. |
| ExperimentException | Learning / Governance | OFARM_OWNED | Exception/governance concepts as anchors only | OFARM uses `ExperimentException` | OFARM needs bounded exceptions to experiment protocols without deleting the underlying rule. |

### CP13 alignment consequences

CP13 concepts are OFARM-owned because they govern how learning, experimentation, causal evidence, and farm memory affect OFARM recommendations, outputs, review, and future high-consequence use.

External scientific, statistical, agronomic-trial, model-evaluation, or experiment-design standards may be used as anchors, profiles, methods, evidence sources, or companion-policy references. They do not become hidden OFARM truth, hidden farm memory, hidden authority, or hidden deployment law.

CP13 alignment does not promote CP14 farm-to-farm intelligence, federated learning, regional alerts, or derivative model-use concepts. CP13 alignment does not promote CP15 model/software deployment, generated-code, SBOM, rollback, canary, or deployment-promotion concepts.

Residual debt: CP13 machine-contract schemas, conformance fixtures, hostile review, learning-metric profile examples, farmer-facing memory display validation, and implementation evidence remain outside active alignment until separately produced and reviewed.
```

### Reason for the change

The Alignment Register must recognise new CP13 constitutional concepts before they are treated as core OFARM concepts.

### Interaction with existing law

This is additive and follows the CP11/CP12 alignment-addendum pattern.

### Risk of contradiction

Low. The main risk is over-owning concepts that should be external; the mitigation is to classify external statistical/scientific standards as anchors/profiles only.

### Baseline law now or RFC law?

Alignment rows belong in baseline. Detailed schema/field semantics remain RFC/machine-contract.

### Migration note

Existing local-knowledge or agent-memory terms remain separate until mapped into CP13.

### Conformance implication

Machine-contract and fixture names should match these concept names.

---

# 5. File: `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

## 5.1 Patch C13-R-1 — Add CP13 readiness and non-claim addendum

### Exact section to add or amend

Append after the CP12 readiness addendum:

```text
## CP13 Learning, Experimentation, and Farm Memory readiness and claim-limit addendum — 2026-05-29
```

### Proposed normative text

```text
## CP13 Learning, Experimentation, and Farm Memory readiness and claim-limit addendum — 2026-05-29

### Readiness posture

CP13 improves the active baseline by adding a governed learning, experimentation, causal-evidence, farm-memory, seasonal-learning, and learning-output qualification layer.

CP13 is a model/runtime governance closure. It is not production autonomous self-improvement, production agronomic advice certification, farm-to-farm intelligence readiness, model deployment readiness, or generated-software delivery readiness.

The correct post-CP13 posture remains:

`implementation-directed with bounded debt.`

### Evidence currently available

CP13 currently provides or proposes:

- a draft CP13 RFC;
- baseline patch text for Constitution, Platform Runtime, Alignment Register, readiness, and hostile-review addenda;
- candidate machine-contract families for later Phase 5;
- candidate conformance fixture families for later Phase 5/6;
- explicit deferrals to CP14 and CP15.

This is design and governance evidence. It is not production runtime evidence, live farm-trial evidence, external scientific-method validation, production causal inference validation, farmer-facing memory UX validation, model deployment evidence, or farm-to-farm learning evidence.

### Claims allowed after CP13 baseline acceptance

After CP13 is accepted and reconciled, the package may claim:

- bounded model-law support for governed learning, experimentation, causal evidence, and farm memory;
- explicit separation between learning output and truth;
- explicit separation between agent memory and farm memory;
- explicit separation between experiment protocol and operation/mission authority;
- explicit promotion law for farm memory candidates;
- explicit retrieval qualification for farm memory use;
- explicit CP11 and CP12 preservation where learning depends on charter-sensitive or mission-sensitive inputs;
- explicit deferral of CP14 farm-to-farm intelligence and CP15 generated-software/model-deployment governance.

### Claims still blocked after CP13

The package must not claim:

- production autonomous self-improvement readiness;
- production agronomic advice certification;
- autonomous experiment design or execution readiness;
- autonomous learning-promotion readiness;
- farm-to-farm intelligence readiness;
- federated learning readiness;
- regional alert readiness;
- benchmark exchange readiness;
- derivative model-use readiness;
- model deployment readiness;
- generated-software readiness;
- generated adapter deployment readiness;
- CP14 readiness;
- CP15 readiness;
- legal, insurance, certification, or regulatory advice;
- livestock-specific learning readiness.

### Evidence required for stronger claims

Stronger CP13 claims require:

- accepted CP13 machine contracts;
- passing CP13 conformance fixtures;
- runtime policy logs showing learning-governance gate execution;
- trace retrieval for `LearningEvaluationTrace`;
- test cases proving farm memory cannot be used outside scope without qualification;
- test cases proving agent memory cannot become farm memory;
- test cases proving experiment protocol does not authorise operations or missions;
- test cases proving causal estimates do not create Compliance Twin facts;
- farmer-facing comprehension and burden validation for farm-memory retrieval, invalidation, uncertainty, and learning-output limitations;
- real-world pilot or simulated-trial evidence before any production autonomous self-improvement claim.

### Explicit deferrals

CP13 defers CP14 farm-to-farm intelligence, federated learning, cross-farm benchmark exchange, regional alerts, derivative model use, aggregation-floor, and re-identification-risk governance.

CP13 defers CP15 generated software, model deployment, adapter generation, canary, rollback, SBOM, build provenance, model-card, and deployment-promotion governance.
```

### Reason for the change

CP13 may look like “self-improving platform readiness.” The readiness memo must prevent that overclaim.

### Interaction with existing law

This preserves the existing implementation-directed/bounded-debt maturity posture and mirrors CP11/CP12 claim-limit addenda.

### Risk of contradiction

Low.

### Baseline law now or RFC law?

Readiness/non-claim posture belongs in baseline.

### Migration note

Do not update product, investor, AI-agent, or developer-facing language to say OFARM is self-improving in production merely because CP13 is accepted.

### Conformance implication

No CP13 runtime or current/default contract claim without conformance and steward evidence.

---

# 6. File: `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

## 6.1 Patch C13-H-1 — Add CP13 hostile-review addendum

### Exact section to add or amend

Append after the CP12 hostile-review update:

```text
## CP13 Learning, Experimentation, and Farm Memory hostile-review addendum — 2026-05-29
```

### Proposed normative text

```text
## CP13 Learning, Experimentation, and Farm Memory hostile-review addendum — 2026-05-29

A hostile reader should treat CP13 as a bounded learning-governance extension, not as proof that OFARM can autonomously learn, experiment, deploy models, or certify agronomic advice in production.

### Hostile-reader verdict

CP13 is the correct next bounded amendment after CP11 and CP12 if it remains learning, experimentation, causal-evidence, farm-memory, and learning-output governance.

CP13 must not become generic AI memory, cross-farm intelligence, federated learning, model deployment governance, generated-software delivery governance, or autonomous self-improvement readiness.

### Closed or substantially reduced by CP13

CP13 closes or reduces the following gaps:

- learning-output-as-truth risk;
- experiment-result-as-causal-fact risk;
- farm-memory-as-hidden-current-state risk;
- agent-memory-as-farm-memory risk;
- causal-estimate-as-compliance-fact risk;
- model-improvement-as-deployment-authority risk;
- mission/operation-records-as-learning-law risk;
- post-hoc outcome-hacking risk;
- farm-memory retrieval outside scope without qualification;
- learning promotion without governance;
- CP11 risk/regret budget use without learning boundary;
- CP12 mission evidence reuse without truth-boundary protection.

### Still open and hostile-reader relevant

CP13 does not close:

- production autonomous self-improvement readiness;
- production agronomic advice certification;
- farm-to-farm intelligence, federated learning, regional alerts, benchmark exchange, or derivative model-use law;
- generated-software delivery, model deployment, adapter deployment, canary, rollback, SBOM, build provenance, or model-card governance;
- external scientific-method validation or universal causal-inference standardisation;
- farmer-facing farm-memory UX validation;
- livestock-specific learning law;
- live farm-trial validation;
- implementation/runtime evidence for CP13 gates until conformance and steward review exist.

### Hostile-reader risks after CP13

The main remaining risks are:

- treating a causal estimate as stronger than its design/evidence supports;
- treating farm memory as current state;
- retrieving memory outside scope without limitation;
- treating agent memory or vector memory as governed farm memory;
- using CP12 mission telemetry as learning truth without evaluation;
- using CP11 regret budget as authority to experiment;
- allowing agents to approve learning promotion;
- hiding uncertainty, missingness, or post-hoc outcome changes;
- letting learning outputs become claim basis, mission authority, or deployment authority;
- overclaiming autonomous self-improvement before implementation evidence exists.

### Hostile-review conclusion

CP13 should be accepted only if it preserves OFARM truth law, Advisory/Compliance separation, CP11 charter gates, CP12 mission gates, human-governed defaults, explicit promotion law, farm-memory retrieval qualification, and draft/non-default machine-contract currentness until a later promotion decision.

### Explicit deferrals

CP13 does not create:

- CP14 farm-to-farm intelligence, federated learning, regional alert, cross-farm benchmark, derivative model-use, aggregation-floor, or re-identification-risk law;
- CP15 generated-software, model deployment, adapter generation, canary, rollback, SBOM, build provenance, model-card, or deployment-promotion law;
- production autonomous self-improvement readiness;
- production agronomic advice certification;
- livestock-specific learning law.

### CP13 exact non-claim wording — 2026-05-29

CP13 does not claim production autonomous self-improvement readiness, production agronomic advice certification, autonomous experiment execution readiness, autonomous learning-promotion readiness, farm-to-farm intelligence readiness, federated learning readiness, regional alert readiness, benchmark exchange readiness, derivative model-use readiness, model deployment readiness, generated-software readiness, CP14 readiness, CP15 readiness, legal advice, insurance advice, certification advice, or livestock-specific learning readiness.
```

### Reason for the change

The hostile-review memo must record what CP13 closes and what remains open. CP13 is especially vulnerable to overclaim because “learning” sounds like autonomous improvement.

### Interaction with existing law

This mirrors CP11 and CP12 hostile-review addendum style and preserves non-claims.

### Risk of contradiction

Low.

### Baseline law now or RFC law?

Hostile-review posture belongs in baseline.

### Migration note

Use this as the Phase 6 hostile-review benchmark. Do not let CP13 acceptance be used as evidence of production learning readiness.

### Conformance implication

CP13 hostile review must test every listed risk before final merge.

---

# 7. Baseline patch cross-check

## 7.1 What CP13 baseline patch must preserve

```text
- assertion/history-first canonical truth;
- governed current-state materialisation;
- one semantic substrate / two logical twins;
- no hidden truth stores;
- no AI-output truth bucket;
- no tool-call success as governance success;
- pack law and fail-closed merge posture;
- default-deny authority;
- human-governed defaults for high-consequence decisions;
- QuerySpecification / QueryPlanIR;
- PassportView / DocumentAssembly output boundaries;
- CP11 charter-sensitive gates;
- CP12 mission-envelope gates;
- draft/non-default currentness for CP11/CP12 machine contracts.
```

## 7.2 What CP13 baseline patch must not do

```text
- promote CP13 RFC to accepted law before hostile review;
- create CP13 machine schemas in Phase 4;
- promote any draft/non-default schema to current/default;
- define CP14 farm-to-farm intelligence;
- define CP15 generated-software/model-deployment governance;
- authorise experiments, operations, or missions by protocol alone;
- make farm memory hidden current state;
- make agent memory farm memory;
- make causal estimates Compliance Twin facts;
- make learning outputs claim basis, mission authority, or deployment authority by default.
```

---

# 8. Conformance implications to carry into Phase 5

The baseline patch creates the following minimum CP13 conformance families:

```text
hypothesis_does_not_create_fact
experiment_protocol_does_not_authorise_operation
experiment_protocol_does_not_authorise_mission_dispatch
risk_budget_does_not_authorise_experiment
regret_budget_does_not_authorise_experiment
outcome_observation_set_does_not_create_causal_estimate
causal_estimate_does_not_create_compliance_fact
causal_estimate_discloses_uncertainty_and_scope
farm_memory_requires_learning_promotion_decision
farm_memory_does_not_create_current_state
farm_memory_retrieval_outside_scope_requires_qualification
agent_memory_cannot_be_farm_memory
seasonal_learning_summary_does_not_update_truth
learning_output_cannot_be_claim_basis_without_separate_gate
learning_output_cannot_be_mission_authority
cp12_telemetry_cannot_create_learning_truth
cp12_verification_can_be_learning_evidence_candidate_only
cp11_charter_sensitive_learning_requires_charter_gate
learning_promotion_by_agent_without_authority_fails
cross_farm_learning_use_defers_to_cp14
model_deployment_use_defers_to_cp15
```

---

# 9. Migration plan

Recommended order:

```text
1. Keep CP13 RFC as draft candidate.
2. Apply Constitution CP13 addendum as candidate baseline patch text only after Phase 6/7 acceptance.
3. Apply Platform Runtime CP13 addendum as candidate baseline patch text only after Phase 6/7 acceptance.
4. Apply Alignment Register CP13 rows only when CP13 terms are accepted as baseline-recognised concepts.
5. Apply Readiness and Hostile Review addenda only when CP13 has completed hostile review and remediation.
6. In Phase 5, create CP13 draft/non-default machine contracts.
7. In Phase 6, hostile-review CP13 contracts and conformance.
8. In Phase 7, assemble final amendment candidate and run final gate.
9. Do not begin CP14 until CP13 steward acceptance passes.
```

---

# 10. Phase 4 conclusion

CP13 baseline patch should proceed to Phase 5 machine-contract planning, but it should not be merged yet.

The baseline patch is correctly bounded if it does only this:

```text
- makes CP13 learning/farm-memory law visible in baseline;
- adds CP13 concepts to the Alignment Register;
- adds runtime learning-governance gates;
- preserves CP11 and CP12;
- blocks learning output from becoming truth, claim basis, mission authority, or deployment authority;
- blocks agent memory from becoming farm memory;
- blocks farm memory from becoming hidden current state;
- preserves CP14/CP15 deferrals;
- updates readiness and hostile-review non-claims.
```

Recommended next command:

```text
Start CP13 Phase 5.

Create the CP13 machine-contract plan.

For each proposed contract, provide:
- contract name;
- purpose;
- required fields;
- optional fields;
- validation rules;
- lifecycle;
- authority source;
- relation to events;
- relation to current-state materialisation;
- relation to Advisory Twin;
- relation to Compliance Twin;
- relation to CP11 charter gates;
- relation to CP12 mission/operation evidence;
- relation to agent memory and model learning;
- relation to CP14/CP15 deferrals;
- conformance tests;
- examples.

Then produce draft schema-style definitions in OFARM-compatible form.

Do not create farm-to-farm intelligence contracts except as forward references to CP14.
Do not create generated-software or model-deployment contracts except as forward references to CP15.
Do not promote CP11 or CP12 draft/non-default schemas to current/default.
Do not claim production autonomous self-improvement readiness.
```


---

# CP13 Phase 7 reconciliation addendum — 2026-05-29

This final baseline patch candidate incorporates the Phase 6.1 remediation without broad rewrite. The baseline should receive only invariant-level language:

- learning output is not truth;
- experiment result is not automatic causal fact;
- farm memory is not hidden current state;
- agent memory is not farm memory;
- causal estimate is not compliance fact;
- model improvement is not deployment authority;
- experiment protocols and trial designs do not authorise operations or CP12 missions;
- CP11/CP12 records may be evidence candidates for learning but do not become learning law by existence;
- CP14 and CP15 remain explicit deferrals.

Detailed machine-field semantics remain in the CP13 RFC, draft/non-default schemas, and conformance runner.
