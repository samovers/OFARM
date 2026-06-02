# OFARM Learning, Experimentation, and Farm Memory RFC v0.1

Date: 2026-05-28  
Status: accepted/merged CP13 RFC; active accepted RFC law subordinate to active baseline; CP13 machine contracts remain draft/non-default  
Target path: `02_accepted_rfcs/OFARM_Learning_Experimentation_and_Farm_Memory_RFC_v0_1.md`  
Authority tier if accepted: accepted RFC; subordinate to `00_active_baseline/` and above companion artifacts under `PROJECT_AUTHORITY.md`  
Scope: introduce a bounded learning, experimentation, causal-evidence, farm-memory, seasonal-learning, and learning-promotion contract layer without reopening OFARM truth, current-state, pack, authority, output, agent, CP11 sustainability-charter, or CP12 cyber-physical mission law.

---

## 1. Purpose

OFARM already has the semantic and governance spine required to protect farm truth:

- assertion/history-first canonical truth;
- governed current-state materialisation;
- one semantic substrate with Compliance Twin and Advisory Twin partitions;
- explicit authority, delegation, sharing, revocation, and default-deny posture;
- pack/profile law;
- query/output qualification and high-consequence output gates;
- sponsor-bound software-agent actorship;
- bounded agent run, trace, blocked-action, tool-manifest, and handoff law;
- Advisory-only world-model and scenario contracts;
- CP11 Sustainable Autonomous Farming Charter governance for sustainability-sensitive constraints, objectives, evidence, claims, exceptions, breaches, and output qualification;
- CP12 Cyber-Physical Mission Envelope governance for mission identity, preflight, dispatch, command integrity, geofence/no-go-zone discipline, emergency stop, human override, telemetry, execution receipt, verification, and physical-safety incident handling.

That foundation is necessary but not sufficient for a self-improving farming platform.

A future OFARM runtime may learn from observations, missions, executed operations, outcomes, seasons, experiments, field trials, agent analyses, world-model scenarios, CP11 charter evaluations, CP12 mission verification, and farmer/advisor review. Without explicit learning law, the platform can fail at a different high-consequence boundary:

```text
operation / mission / seasonal outcome / model output / agent memory / experiment result
→ silently treated as causal truth or reusable farm memory
→ future recommendations, claims, missions, or optimisation decisions depend on it
```

This RFC introduces the first CP13 contract layer for **Learning, Experimentation, and Farm Memory**.

The core decision is:

```text
Learning output is not truth.
Experiment result is not automatic causal fact.
Farm memory is not hidden current state.
Agent memory is not farm memory.
Causal estimate is not compliance fact.
Model improvement is not deployment authority.
Mission or operation records may inform learning, but they do not become learning law by themselves.
```

CP13 makes learning governable. It does not make OFARM autonomously self-improving in production.

---

## 2. Scope

This RFC covers learning, experimentation, causal evidence, farm memory, and seasonal learning for crop-farming OFARM contexts already within the active baseline scope.

It defines:

- CP13 authority, scope, and non-goals;
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
- `ExperimentException`;
- interaction with CP11 `RiskBudget` and `RegretBudget` hooks;
- interaction with CP11 charter gates;
- interaction with CP12 mission and operation evidence;
- separation between agent memory, training data, model updates, and OFARM farm memory;
- learning-specific authority actions;
- learning event grammar and commit-matrix implications;
- learning pack/profile surface implications;
- machine-contract implications;
- conformance implications;
- readiness and non-claims;
- explicit deferrals to CP14, CP15, and future domains.

This RFC applies to **learning-sensitive uses**, including:

- creation of a testable learning hypothesis;
- creation or approval of an experiment protocol;
- design of a field trial, strip trial, split-field comparison, operational A/B comparison, or mission/operation comparison;
- definition of outcome measures used for learning or causal evaluation;
- ingestion or grouping of outcome observations for learning;
- creation of a causal estimate;
- creation of a learning evaluation trace;
- promotion of a learning result to farm memory;
- retrieval or use of farm memory in recommendations, planning, advisory outputs, charter-sensitive evaluations, or mission preparation;
- seasonal learning summaries;
- learning-derived recommendations;
- agent learning and memory interactions;
- learning-related use of CP11 risk/regret budgets;
- learning-related use of CP12 mission telemetry, execution receipt, verification, near-miss, or safety-incident data;
- learning-related pack/profile activation;
- learning outputs that may influence high-consequence decisions, claims, or future autonomous workflows.

---

## 3. Non-goals

This RFC does **not**:

1. Rewrite the OFARM Constitution.
2. Reopen assertion/history-first canonical truth.
3. Reopen governed current-state materialisation.
4. Reopen the Compliance Twin / Advisory Twin split.
5. Reopen pack merge law except for learning-specific surface-family additions or mappings.
6. Reopen core authority law except for learning-specific action-class additions or mappings.
7. Reopen CP11 Sustainable Autonomous Farming Charter law.
8. Reopen CP12 Cyber-Physical Mission Envelope law.
9. Create autonomous compliance decisioning.
10. Create robot, machine, drone, actuator, or physical mission execution authority.
11. Create autonomous self-improvement readiness.
12. Create production agronomic advice certification.
13. Create legal, certification, insurance, or regulatory advice.
14. Define farm-to-farm intelligence, federated learning, regional alerts, benchmark exchange, derivative model-use policy, or cross-farm learning exchange.
15. Define generated-software deployment, model deployment, adapter generation, canary promotion, rollback, SBOM, build provenance, or software-supply-chain governance.
16. Treat agent memory, model weights, vector-store memory, prompt history, or tool-call history as OFARM farm memory.
17. Treat a world-model scenario, model output, statistical estimate, or agent explanation as causal truth by itself.
18. Treat an experiment protocol as authority to conduct operations or missions.
19. Treat CP11 `RiskBudget` or `RegretBudget` as authority to experiment by itself.
20. Treat CP12 mission telemetry, execution receipt, or mission verification as learning truth by itself.
21. Expand OFARM from crop-farming operational law into livestock-specific learning, animal-welfare, herd/flock, feeding, treatment, or animal-health learning law.
22. Define a universal agronomic experiment methodology or universal natural-science standard for causal inference.
23. Define production-ready automated trial design or autonomous experimental intervention.

The full farm-to-farm intelligence, federated learning, cross-farm benchmarking, regional-alert, derivative model-use, aggregation-floor, and re-identification-risk model belongs to **CP14**.

The full agentic software delivery, generated adapter/model deployment, rollout, canary, rollback, SBOM, build provenance, model-card, and deployment-promotion governance layer belongs to **CP15**.

---

## 4. Authority relationship to the Constitution

If this RFC is accepted, it extends the active Constitution by introducing a learning, experimentation, causal-evidence, and farm-memory layer.

The Constitution remains higher authority. This RFC must be interpreted under existing constitutional invariants:

- canonical truth is assertion/history-first;
- current state is governed materialisation, not hidden truth;
- Advisory Twin and Compliance Twin remain logical partitions over one semantic substrate;
- events do not change current state merely by existing;
- promotion requires declared safe paths;
- packs cannot mutate core meaning by stealth;
- external payloads are not hidden OFARM law;
- AI outputs, agent memory, tool success, manifests, generated summaries, model outputs, vector memories, and scenario states are not hidden truth stores or hidden governance decisions;
- authority is action-class-specific and default-deny;
- high-consequence use requires evidence, freshness, authority, and output qualification;
- CP11 charter-sensitive use remains subject to CP11 where material;
- CP12 mission-sensitive use remains subject to CP12 where material.

CP13 adds one constitutional invariant:

```text
No learning artifact, experiment result, causal estimate, seasonal summary, farm memory entry, agent memory item, model output, or local memory rule may become canonical truth, current state, Compliance Twin fact, claim basis, mission authority, or deployment authority merely by existing.
```

A learning artifact may affect harder OFARM outcomes only through explicit authority, evidence, review, promotion, output, current-state, CP11, CP12, and later CP14/CP15 gates where applicable.

---

## 5. Authority relationship to Platform Runtime

The Platform Runtime must realise CP13 through deterministic enforcement points.

For learning-sensitive use, the runtime must be able to:

- resolve the applicable `LearningScope`;
- distinguish hypothesis, protocol, trial design, outcome measure, outcome observation, evidence bundle, causal estimate, learning evaluation trace, promotion decision, farm memory entry, seasonal summary, and learning output;
- evaluate authority for learning-specific action classes;
- prevent agent memory, model state, prompt history, tool results, vector stores, scenario outputs, and generated summaries from becoming farm memory by stealth;
- prevent experiment protocols and trial designs from authorising physical operations or missions;
- enforce CP11 charter constraints, objectives, evidence requirements, risk budgets, regret budgets, and claim/output limits where learning materially affects sustainability-sensitive use;
- enforce CP12 mission-envelope requirements where an experiment or learning workflow involves cyber-physical mission execution;
- link outcome observations to evidence basis, missingness, data quality, measurement method, and scope;
- distinguish correlation, association, exploratory result, causal estimate, and promoted farm memory;
- record `LearningEvaluationTrace` where a learning output affects recommendation, promotion, claim, review, seasonal summary, output qualification, or future high-consequence reliance;
- preserve farm memory invalidation, expiry, supersession, and retrieval qualification;
- qualify learning-derived outputs with allowed and prohibited uses;
- keep cross-farm intelligence and model/software deployment out of CP13 unless CP14 or CP15 later authorises them.

The runtime may optimise storage, indexes, caches, retrieval methods, summary generation, model evaluation, and learning workflows. It may not optimise by flattening learning artifacts into current state, Compliance Twin facts, authority grants, execution authority, claim basis, or deployment authority.

---

## 6. Definitions

| Term | CP13 meaning |
|---|---|
| Learning-sensitive use | A use where learning artifacts, experiment results, causal estimates, farm memory, seasonal summaries, or agent/model learning may materially affect recommendation, planning, claim, review, mission preparation, output, or future high-consequence reliance. |
| LearningScope | Spatial, temporal, biological, operational, equipment, evidence, and reuse boundary for a learning artifact. |
| LearningHypothesis | A testable proposition about farm behaviour, intervention effect, mission behaviour, environmental response, risk, or outcome. |
| ExperimentProtocol | Governed protocol for testing a hypothesis or comparing treatments, controls, operations, or missions. It is not operation or mission authority. |
| TrialDesign | Design structure for an experiment, including experimental units, treatment arms, control/comparison basis, randomisation/blocking where applicable, outcome measures, and analysis posture. |
| ExperimentalUnit | The unit of comparison or assignment in a trial, such as field strip, plot, zone, crop-cycle segment, mission segment, lot, or other scoped unit. |
| TreatmentArm | A planned treatment, intervention, mission, operation, input, timing, rate, or management difference under comparison. |
| ControlCondition | Baseline, untreated, standard-practice, counterfactual, historical, matched, or modelled comparison condition. |
| OutcomeMeasureSpec | Predeclared measure used to evaluate learning, such as yield, quality, input use, soil indicator, disease pressure, mission success, crop damage, water use, energy use, margin, or charter-sensitive indicator. |
| OutcomeObservationSet | Grouped outcome observations for a learning scope, measure, unit, treatment, or comparison. It is evidence input, not a causal conclusion by itself. |
| LearningEvidenceBundle | Evidence bundle used to support a learning evaluation, causal estimate, seasonal learning summary, or farm memory promotion decision. |
| LearningEvaluationTrace | Trace showing how learning evidence, scope, design, assumptions, missingness, uncertainty, comparison basis, and policy gates were evaluated. |
| CausalEstimate | Qualified estimate of treatment/operation/mission/context effect. It is not causal truth or Compliance Twin fact by itself. |
| LearningPromotionDecision | Governance decision determining whether a learning result may become farm memory, remain advisory, require more evidence, be rejected, be invalidated, or be superseded. |
| FarmMemoryEntry | Governed, scoped, evidence-linked, invalidation-aware memory about farm-specific behaviour or experience. It is not hidden current state. |
| FarmMemoryInvalidationRule | Rule that causes a farm memory entry to expire, be downgraded, require review, or be invalidated when context changes or evidence contradicts it. |
| FarmMemoryRetrievalQualification | Required qualification when farm memory is retrieved for use in recommendation, planning, output, agent reasoning, or review. |
| SeasonalLearningSummary | Season-bounded learning summary linking observations, operations, missions, outcomes, hypotheses, and decisions. It is not a blanket truth update. |
| LearningOutputQualification | Allowed/prohibited-use qualification for learning-sensitive outputs. |
| ExperimentRollbackTrigger | Condition under which an experiment, trial, or learning workflow should stop, roll back, downgrade, or require review. |
| ExperimentException | Governed, bounded exception to an experiment protocol or learning-policy rule. |
| Agent memory | Memory, state, context, vector store, prompt history, or model-specific retained context used by a software agent. It is not OFARM farm memory. |
| Model improvement | Change to model, prompt, workflow, weights, parameters, adapter, or generated code. It is not deployment authority and belongs partly to CP15 when deployment is involved. |

---

## 7. CP13 learning artifact family

CP13 defines a learning artifact family. These artifacts are not hidden truth stores.

The CP13 family includes:

```text
LearningScope
LearningHypothesis
ExperimentProtocol
TrialDesign
ExperimentalUnit
TreatmentArm
ControlCondition
RandomizationPlan
BlockingFactor
OutcomeMeasureSpec
OutcomeObservationSet
LearningEvidenceBundle
LearningEvaluationTrace
CausalEstimate
LearningPromotionDecision
FarmMemoryEntry
FarmMemoryInvalidationRule
FarmMemoryRetrievalQualification
SeasonalLearningSummary
LearningOutputQualification
ExperimentRollbackTrigger
ExperimentException
```

Each CP13 artifact must declare:

- artifact identity;
- version or revision where applicable;
- authority/source basis;
- `LearningScope` or explicit reason scope is inherited;
- target twin posture;
- evidence basis where applicable;
- allowed uses;
- prohibited uses;
- lifecycle state;
- invalidation/supersession posture where applicable;
- relation to current state, CP11, CP12, CP14, or CP15 where applicable.

No CP13 artifact becomes canonical truth or current state merely by existing.

---

## 8. Learning scope and locality boundary

`LearningScope` is required for high-consequence CP13 artifacts and recommended for all CP13 artifacts.

A `LearningScope` must identify the boundary within which a learning statement may be interpreted. The scope may include:

- farm/tenant;
- field, parcel, management zone, strip, plot, trial block, or mission segment;
- crop, variety, crop cycle, season, lot, or harvest context;
- soil, weather, topography, irrigation, pest/disease, and management context;
- operation, intervention, mission, input programme, or machine context;
- experimental units and comparison basis;
- time interval and validity horizon;
- evidence basis and missingness context;
- allowed reuse boundary;
- prohibited reuse boundary;
- whether the learning is local/farm-scoped, profile-scoped, advisory-only, or eligible for later CP14 exchange.

Default posture:

```text
CP13 learning is local/farm-scoped unless CP14 explicitly governs cross-farm use.
```

A farm memory entry or causal estimate must not be reused outside its declared `LearningScope` without a retrieval qualification, scope-expansion review, or later CP14-governed exchange mechanism.

---

## 9. Learning hypothesis lifecycle

A `LearningHypothesis` is a testable proposition. It is not fact.

A hypothesis should declare:

- hypothesis statement;
- expected effect direction and magnitude if known;
- scope;
- assumptions;
- comparison basis;
- candidate evidence sources;
- intended evaluation method;
- related CP11 charter objectives or constraints where material;
- related CP12 mission/operation evidence where material;
- authority and sponsor;
- allowed uses;
- prohibited uses.

Recommended lifecycle states:

```text
DRAFT
PROPOSED
APPROVED_FOR_EXPLORATION
APPROVED_FOR_EXPERIMENT_PROTOCOL
UNDER_EVALUATION
SUPPORTED
WEAKLY_SUPPORTED
INCONCLUSIVE
CONTRADICTED
REJECTED
SUPERSEDED
WITHDRAWN
```

A supported hypothesis is not automatically a causal estimate, farm memory entry, claim basis, Compliance Twin fact, or operational authority.

---

## 10. Experiment protocol authority and non-authorisation boundary

An `ExperimentProtocol` governs a learning design. It is not operational authority.

An experiment protocol may define:

- hypothesis references;
- learning scope;
- trial design;
- experimental units;
- treatment arms;
- control/comparison conditions;
- randomisation or blocking if applicable;
- outcome measures;
- evidence capture plan;
- data-quality and missingness plan;
- analysis posture;
- CP11 charter applicability and risk/regret budget posture;
- CP12 mission applicability where cyber-physical execution is involved;
- authority and approval posture;
- rollback/abort triggers;
- exception policy;
- output qualification.

An experiment protocol does **not** authorise:

- field operations;
- physical missions;
- robot/machine dispatch;
- input application;
- charter exceptions;
- claim publication;
- farm-to-farm sharing;
- model/software deployment.

Operations still require ordinary OFARM operation/intervention law. Cyber-physical missions still require CP12. Sustainability-sensitive trial actions still require CP11. Cross-farm learning requires CP14. Model/software deployment requires CP15.

---

## 11. Trial design, treatment arms, controls, and outcome-hacking prevention

`TrialDesign` must prevent post-hoc narrative learning from masquerading as experiment-backed learning.

Where a learning artifact claims experimental support, the trial design should declare:

- experimental units;
- treatment arms;
- control/comparison conditions;
- assignment method;
- randomisation method or reason randomisation is not used;
- blocking factors;
- minimum replication or reason replication is not possible;
- planned outcome measures;
- analysis method;
- exclusion criteria;
- missingness handling;
- stopping/rollback criteria;
- charter and safety constraints;
- authority/approval posture.

A `TreatmentArm` is a planned difference under comparison. It is not an executed intervention. Executed interventions must be recorded under existing OFARM operation/execution law and may later be linked as evidence.

A `ControlCondition` may be untreated, standard-practice, historical, matched, synthetic/modelled, or externally referenced. Its type must be declared because causal strength depends on comparison basis.

Outcome-hacking prevention rule:

```text
A learning output must disclose whether outcome measures were predeclared, amended, added post hoc, excluded, or substituted.
```

Post-hoc outcome discovery may be useful, but it must not present itself as predeclared experimental evidence.

---

## 12. Outcome measure specification

`OutcomeMeasureSpec` declares what is measured or evaluated.

Outcome measures may include:

- yield;
- quality;
- protein;
- crop stand;
- crop damage;
- weed pressure;
- pest/disease pressure;
- soil nitrate;
- soil moisture;
- soil organic matter indicator;
- water use;
- energy use;
- input use;
- nutrient-use efficiency;
- margin;
- labour or machine time;
- mission success;
- safety event rate;
- equipment performance;
- biodiversity proxy;
- runoff/leaching proxy;
- emissions estimate;
- CP11 charter-sensitive indicator.

Each outcome measure should declare:

- measure identity;
- unit/quantity kind;
- method;
- measurement or modelling basis;
- spatial scope;
- temporal scope;
- evidence source class;
- evidence quality state;
- freshness state;
- expected precision/uncertainty;
- claim eligibility;
- whether the measure was predeclared or post hoc.

Outcome measures should reuse existing OFARM measurement/evidence and CP11 sustainability metric-profile posture where applicable.

---

## 13. Outcome observation set and missingness handling

`OutcomeObservationSet` groups observations relevant to a learning artifact.

It must preserve:

- observation identities;
- source/evidence references;
- measurement method;
- collection time and spatial scope;
- experimental unit or treatment/control linkage;
- missingness;
- censoring;
- quality state;
- exclusions;
- transformations;
- aggregation method;
- uncertainty;
- provenance.

Missingness is not absence of effect. A learning evaluation must distinguish:

```text
NO_DATA
PARTIAL_DATA
MISSING_BY_DESIGN
MISSING_DUE_TO_FAILURE
MISSING_NOT_RANDOM
CENSORED
DISPUTED
INVALIDATED
```

An outcome observation set is evidence input. It is not a causal estimate or farm memory entry by itself.

---

## 14. Learning evidence bundle

`LearningEvidenceBundle` groups evidence used in a learning evaluation, causal estimate, farm-memory promotion, or seasonal summary.

It may link:

- observations;
- lab results;
- sensor records;
- imagery;
- scouting notes;
- operation records;
- executed intervention consequences;
- CP12 mission telemetry;
- CP12 execution receipts;
- CP12 mission verification;
- CP12 near-miss or physical-safety incident records;
- CP11 charter evaluations;
- outcome observation sets;
- external weather/market/regulatory data;
- farmer/advisor annotations;
- model outputs and scenario results, clearly marked as such.

The bundle must declare evidence quality, missingness, freshness, provenance, and limitations.

Evidence bundle rule:

```text
A learning evidence bundle is not a learning conclusion. It may support a LearningEvaluationTrace, CausalEstimate, SeasonalLearningSummary, or LearningPromotionDecision.
```

---

## 15. Causal estimate and uncertainty boundary

`CausalEstimate` is a qualified estimate of effect. It is not causal truth by itself.

A causal estimate should declare:

- estimand or effect target;
- treatment/control or comparison basis;
- learning scope;
- outcome measure;
- method;
- assumptions;
- evidence bundle;
- missingness and exclusions;
- uncertainty interval or confidence/credibility posture where applicable;
- bias/validity threats;
- external validity boundary;
- result classification;
- allowed uses;
- prohibited uses;
- review/promotion posture.

Result classifications may include:

```text
EXPLORATORY_ASSOCIATION
DESCRIPTIVE_COMPARISON
WEAK_CAUSAL_SIGNAL
CAUSAL_ESTIMATE_WITH_LIMITATIONS
INCONCLUSIVE
CONTRADICTED
INVALIDATED
```

No causal estimate may become a Compliance Twin fact, sustainability claim basis, operational authority, or current-state fact without the applicable review, evidence, authority, output, CP11, and current-state gates.

---

## 16. Learning evaluation trace

`LearningEvaluationTrace` records how a learning result was evaluated.

It should include:

- subject evaluated;
- learning scope;
- hypothesis/protocol/trial references;
- evidence bundle;
- outcome measures;
- comparison/control basis;
- method;
- assumptions;
- missingness;
- bias/validity threats;
- uncertainty;
- CP11 charter gates where material;
- CP12 mission/operation evidence basis where material;
- authority and review state;
- result disposition;
- blocked/review-required reasons;
- output qualification;
- promotion eligibility.

Evaluation dispositions may include:

```text
EXPLORATORY_ONLY
INSUFFICIENT_BASIS
REQUIRE_REVIEW
REQUIRE_MORE_EVIDENCE
ELIGIBLE_FOR_CAUSAL_ESTIMATE
ELIGIBLE_FOR_FARM_MEMORY_PROMOTION
REJECTED
INVALIDATED
SUPERSEDED
```

A learning evaluation trace does not create farm memory or causal truth by itself.

---

## 17. Learning promotion decision

`LearningPromotionDecision` is the governed decision that determines whether a learning result may be promoted, rejected, downgraded, invalidated, or retained as advisory.

Possible outcomes:

```text
REMAIN_ADVISORY
PROMOTE_TO_FARM_MEMORY
PROMOTE_WITH_RETRIEVAL_QUALIFICATION
REQUIRE_MORE_EVIDENCE
REQUIRE_HUMAN_REVIEW
REJECT
INVALIDATE_EXISTING_MEMORY
SUPERSEDE_EXISTING_MEMORY
DOWNGRADE_EXISTING_MEMORY
```

Promotion must consider:

- learning scope;
- evidence sufficiency;
- outcome measure quality;
- causal strength;
- uncertainty;
- missingness;
- charter constraints and risk/regret posture;
- recency/freshness;
- farm context stability;
- human/advisor review where required;
- allowed and prohibited uses;
- invalidation triggers;
- output qualification.

A promotion decision is not a Compliance Twin fact unless a separate Compliance Twin path explicitly promotes it under existing OFARM law.

---

## 18. Farm memory entry

`FarmMemoryEntry` is governed farm-specific memory. It is not agent memory, hidden current state, or automatic truth.

A farm memory entry should declare:

- memory statement;
- memory type;
- learning scope;
- evidence bundle;
- promotion decision;
- causal estimate or learning evaluation basis where applicable;
- confidence/strength;
- uncertainty;
- validity horizon;
- retrieval qualification;
- invalidation rules;
- supersession links;
- allowed uses;
- prohibited uses;
- Advisory/Compliance posture;
- whether it may inform recommendations, planning, CP11 evaluation, CP12 mission preparation, or output generation.

Example farm memory entry statements:

```text
Field A has historically shown poor response to late nitrogen under dry spring conditions.
This management zone compacts after heavy rainfall and should be avoided by heavy machinery until soil condition evidence improves.
Variety X performed well after cover crop Y in the previous two comparable seasons.
Robot R2 produced crop-damage incidents in this slope/soil/moisture context.
Pest pressure in this block tends to rise after mild winters, but evidence is advisory and locally scoped.
```

A farm memory entry must always remain retrievable with its evidence basis and limitations.

---

## 19. Farm memory invalidation

`FarmMemoryInvalidationRule` defines when a memory should expire, downgrade, require review, or be invalidated.

Triggers may include:

- crop/variety change;
- rotation change;
- soil management change;
- drainage/irrigation change;
- field boundary change;
- equipment/robot change;
- sensor calibration issue;
- new contradictory evidence;
- season/time horizon expiry;
- climate/weather regime shift;
- pest/disease ecology change;
- CP11 charter change;
- CP12 mission/safety incident;
- pack/profile change;
- authority revocation;
- evidence invalidation;
- farmer/advisor dispute.

Default posture:

```text
A farm memory entry that has an active invalidation trigger must not be used for high-consequence recommendation, claim, mission preparation, or Compliance Twin bridging unless reviewed or requalified.
```

---

## 20. Farm memory retrieval qualification

`FarmMemoryRetrievalQualification` is required when farm memory is retrieved for learning-sensitive or high-consequence use.

It should expose:

- memory entry identity;
- learning scope;
- current retrieval context;
- scope match/mismatch;
- freshness/validity state;
- evidence strength;
- invalidation status;
- uncertainty;
- Advisory/Compliance posture;
- allowed uses;
- prohibited uses;
- whether review is required;
- whether current-state or CP11/CP12 gates are also required.

Retrieval rule:

```text
Farm memory retrieval is not authority to act. It is qualified context that may inform recommendation, review, planning, or evidence request.
```

---

## 21. Seasonal learning summary

`SeasonalLearningSummary` summarizes learning over a season or crop cycle.

It may include:

- hypotheses proposed/tested;
- experiment protocols run;
- trial designs and actual execution coverage;
- outcome measures;
- evidence bundles;
- causal estimates;
- farm memory promotion decisions;
- rejected or invalidated learning;
- CP11 charter outcomes;
- CP12 mission outcomes and safety events;
- unresolved questions;
- evidence needs;
- recommendations for future review.

A seasonal learning summary is not a blanket update of farm truth. It may propose farm memory entries, evidence needs, or review actions, but those must follow CP13 promotion law.

---

## 22. Learning output qualification

`LearningOutputQualification` qualifies learning-sensitive outputs.

It must distinguish:

```text
EXPLORATORY
ADVISORY_ONLY
DESCRIPTIVE_SUMMARY
EXPERIMENT_RESULT_SUMMARY
CAUSAL_ESTIMATE_CANDIDATE
FARM_MEMORY_CANDIDATE
FARM_MEMORY_PROMOTED
SEASONAL_SUMMARY
REQUIRES_REVIEW
INSUFFICIENT_BASIS
```

It must expose:

- learning scope;
- evidence basis;
- method/analysis basis;
- uncertainty;
- missingness;
- causal strength;
- farm-memory status;
- invalidation posture;
- Advisory/Compliance posture;
- allowed uses;
- prohibited uses;
- current-state reliance if any;
- CP11/CP12 reliance if any;
- sharing/disclosure posture;
- review/promotion posture.

Learning outputs must not claim:

- canonical truth;
- Compliance Twin fact;
- execution truth;
- mission authority;
- sustainability claim basis;
- cross-farm validity;
- model/software deployment authority;

unless a separate applicable OFARM path explicitly supports that use.

---

## 23. CP11 RiskBudget and RegretBudget integration

CP11 introduced `RiskBudget` and `RegretBudget` as draft/non-default hooks. CP13 may use these hooks, but must not treat them as authority by themselves.

CP13 rule:

```text
RiskBudget and RegretBudget may bound learning and experimentation. They do not authorise experimentation, intervention, mission dispatch, charter exception, or model/software deployment by themselves.
```

A learning workflow involving risk/regret budgets should declare:

- budget reference;
- scope;
- approved authority basis;
- exposure or downside tracked;
- stopping/rollback triggers;
- CP11 charter constraints;
- CP12 mission constraints if physical missions are involved;
- review/approval gates;
- remaining budget state;
- prohibited uses.

CP13 may propose machine-contract refinements for risk/regret integration, but CP11 draft/non-default status must not be converted to current/default as part of CP13 unless a separate currentness promotion explicitly approves it.

---

## 24. CP11 charter gate integration

Learning and experimentation must respect CP11.

CP13 artifacts are charter-sensitive when they materially affect:

- sustainability-sensitive recommendations;
- sustainability claims;
- charter exceptions;
- charter breaches;
- risk/regret budgets;
- sustainability objectives;
- experiment design involving environmental/input/soil/water/biodiversity risks;
- future execution-bound plans.

Where CP11 applies, CP13 must link to CP11 charter applicability context, policy evaluation trace, evidence requirements, claim-basis rules, output qualification, exception posture, and breach posture as relevant.

A learning result cannot weaken CP11 constraints, convert a charter exception into a permanent rule change, or justify a sustainability claim without the normal CP11 claim-basis and output gates.

---

## 25. CP12 mission and operation records as learning evidence

CP12 mission artifacts may inform CP13 learning. They are not learning conclusions by themselves.

Relevant CP12 evidence candidates include:

- mission preflight traces;
- dispatch authorisations;
- command envelopes and integrity records;
- telemetry envelopes;
- execution receipts;
- mission verification;
- abort events;
- emergency-stop activations;
- remote takeover events;
- near-miss events;
- physical-safety incidents;
- mission output qualifications.

CP13 may use these as evidence if provenance, scope, quality, and limitations are preserved.

Rules:

```text
Telemetry is not outcome truth by itself.
Execution receipt is not verification by itself.
Mission verification is not causal estimate by itself.
Near-miss or incident records are not automatic compliance facts by themselves.
Mission records may support learning only through LearningEvidenceBundle and LearningEvaluationTrace.
```

---

## 26. Agent memory, training data, and farm memory separation

Software agents may keep runtime state, prompt context, vector retrieval memory, tool traces, model context, and agent-specific memory. None of these are OFARM `FarmMemoryEntry` by default.

CP13 must distinguish:

| Layer | Status |
|---|---|
| Agent memory | Runtime/supporting memory for a software agent; not OFARM farm memory. |
| Agent run trace | Governance trace of an agent run; may be evidence input. |
| Training data | Data used to train/evaluate models; not farm memory unless separately governed. |
| Model state/weights | Not OFARM truth, not farm memory, not deployment authority. |
| FarmMemoryEntry | Governed OFARM artifact promoted through CP13 learning-promotion law. |

Agent learning rules:

```text
An agent may propose learning artifacts only within its authority envelope.
An agent may not promote farm memory by default.
An agent may not convert its memory into farm memory by writing a summary.
An agent may not use farm memory outside its retrieval qualification.
An agent may not train or share learning artifacts beyond data-sovereignty, CP14, and CP15 boundaries.
```

`AgentDataLearningPolicy` remains relevant. CP13 should integrate with it rather than replacing it.

---

## 27. Learning-derived recommendations and BridgeCandidate handoff

A learning result may produce a recommendation or proposed next step. It must not bypass recommendation, authority, CP11, CP12, or output gates.

Where a learning-derived result suggests a future action, the appropriate path is usually:

```text
LearningEvaluationTrace / FarmMemoryRetrievalQualification
→ LearningOutputQualification
→ BridgeCandidate or recommendation object
→ applicable preflight/review/authority gates
→ CP11 or CP12 gates where material
```

A learning-derived recommendation is not:

- operation authority;
- mission dispatch authority;
- compliance fact;
- sustainability claim basis;
- farm memory promotion;
- generated-software deployment authority.

---

## 28. Learning-specific authority actions

CP13 adds learning-sensitive action classes to be mapped into the Authority Action Matrix.

Candidate action classes:

```text
LEARNING_PROPOSE_HYPOTHESIS
LEARNING_APPROVE_EXPERIMENT_PROTOCOL
LEARNING_AMEND_EXPERIMENT_PROTOCOL
LEARNING_APPROVE_TRIAL_DESIGN
LEARNING_RECORD_OUTCOME_OBSERVATION_SET
LEARNING_CREATE_EVIDENCE_BUNDLE
LEARNING_CREATE_CAUSAL_ESTIMATE
LEARNING_REVIEW_CAUSAL_ESTIMATE
LEARNING_PROMOTE_FARM_MEMORY
LEARNING_INVALIDATE_FARM_MEMORY
LEARNING_RETRIEVE_FARM_MEMORY_HIGH_CONSEQUENCE
LEARNING_APPROVE_SEASONAL_SUMMARY
LEARNING_APPROVE_EXPERIMENT_EXCEPTION
LEARNING_TRIGGER_ROLLBACK
LEARNING_AUTHORIZE_DATA_USE_FOR_MODEL_TRAINING
```

Default posture:

- agents may propose hypotheses, prepare evidence bundles, generate advisory analyses, and prepare review packages within authority;
- agents may not by default approve experiment protocols, promote farm memory, invalidate farm memory, approve high-consequence retrieval, authorise training data use, or approve cross-farm sharing;
- human/governance approval is required by default for high-consequence experiment protocols, farm-memory promotion, invalidation, and training/sharing actions;
- CP12 authority is required for physical missions;
- CP14 authority is required for cross-farm learning;
- CP15 authority is required for software/model deployment.

---

## 29. Event grammar and commit-matrix implications

CP13 requires learning-specific event and commit handling.

Candidate event families:

```text
LearningHypothesisProposed
LearningHypothesisApprovedForExploration
ExperimentProtocolProposed
ExperimentProtocolApproved
TrialDesignApproved
OutcomeObservationSetRecorded
LearningEvidenceBundleCreated
CausalEstimateCreated
LearningEvaluationTraceRecorded
LearningPromotionDecisionRecorded
FarmMemoryEntryPromoted
FarmMemoryEntryInvalidated
FarmMemoryEntrySuperseded
FarmMemoryRetrievedForUse
SeasonalLearningSummaryCreated
ExperimentRollbackTriggered
ExperimentExceptionRequested
ExperimentExceptionApproved
```

These events do not automatically create harder truth. Commit classes should distinguish:

- note/exploratory learning;
- hypothesis assertion;
- protocol proposal;
- governance decision;
- evidence record;
- advisory learning output;
- causal estimate candidate;
- farm memory promotion decision;
- farm memory entry;
- invalidation/supersession record;
- seasonal summary.

A learning event may influence current-state materialisation only if a separate accepted consequence and current-state law allow it. Most CP13 artifacts remain Advisory Twin or local governed memory.

---

## 30. Pack/profile interaction for learning policy and memory rules

CP13 introduces learning-specific pack/profile surfaces.

Candidate `PackSurfaceFamily` values:

```text
LEARNING_POLICY
EXPERIMENT_PROTOCOL_POLICY
TRIAL_DESIGN_POLICY
OUTCOME_MEASURE_POLICY
CAUSAL_ESTIMATE_POLICY
FARM_MEMORY_PROMOTION_POLICY
FARM_MEMORY_INVALIDATION_POLICY
FARM_MEMORY_RETRIEVAL_POLICY
LEARNING_OUTPUT_QUALIFICATION_POLICY
AGENT_LEARNING_POLICY
```

Recommended merge posture:

- learning evidence requirements: `STRONGEST_REQUIREMENT` where cumulative;
- experiment protocol safeguards: `STRONGEST_REQUIREMENT` or `HARD_FAIL` where conflict exists;
- causal-estimate method profile: `IDENTICAL_ONLY` or `HARD_FAIL` for claim-bearing/high-consequence use if method equivalence is not proven;
- farm-memory promotion policy: `STRONGEST_REQUIREMENT` or `HARD_FAIL`;
- farm-memory invalidation policy: `STRONGEST_REQUIREMENT`;
- retrieval qualification policy: `STRONGEST_REQUIREMENT`;
- agent learning policy: `STRONGEST_REQUIREMENT` for stricter consent/retention/training/sharing controls;
- cross-farm learning pack surfaces: deferred to CP14.

Packs must not weaken evidence requirements, promote farm memory, authorise experiments, authorise missions, authorise cross-farm learning, or authorise model deployment by stealth.

---

## 31. Runtime learning governance gate

The Platform Runtime should add a CP13 learning governance gate for learning-sensitive use.

The gate should evaluate:

- learning scope;
- authority action class;
- evidence basis;
- experiment protocol status;
- outcome measure predeclaration and post-hoc status;
- missingness and data quality;
- causal estimate strength and limitations;
- farm-memory promotion eligibility;
- invalidation status;
- retrieval qualification;
- CP11 charter posture where material;
- CP12 mission/evidence posture where material;
- output qualification;
- CP14/CP15 deferral boundaries.

The gate should emit or link a `LearningEvaluationTrace` when learning affects recommendation, output, promotion, high-consequence retrieval, charter-sensitive use, mission-sensitive use, or seasonal summary.

---

## 32. Interaction with Advisory Twin

By default, CP13 learning artifacts are Advisory Twin material unless explicitly promoted to a governed local/farm-memory artifact or bridged through another accepted OFARM path.

Advisory CP13 artifacts may:

- raise hypotheses;
- summarize evidence;
- compare outcomes;
- propose causal estimates;
- request more evidence;
- propose farm-memory promotion;
- prepare recommendations;
- prepare review packages;
- inform world-model/scenario work.

They may not directly create:

- Compliance Twin facts;
- current state;
- accepted execution consequences;
- mission dispatch authority;
- sustainability claims;
- charter exceptions;
- official attestations;
- filed submissions;
- model/software deployment authority;
- cross-farm intelligence artifacts.

---

## 33. Interaction with Compliance Twin

CP13 does not create automatic Compliance Twin consequences.

A learning artifact may become relevant to Compliance Twin only through existing Compliance Twin gates and an explicit accepted path. Examples:

- a verified learning-derived nonconformity pattern may suggest review;
- a farm memory entry may inform evidence requests;
- a causal estimate may help explain corrective-action effectiveness;
- a seasonal summary may support a dossier only if output qualification and evidence gates are satisfied.

But none of these are compliance facts merely by being learning artifacts.

---

## 34. Interaction with current-state materialisation

Farm memory is not current state.

Current-state materialisation may include or reference CP13 artifacts only if active law and materialisation policy explicitly allow it for a use class. For high-consequence use, freshness and basis must be explicit.

Rules:

```text
FarmMemoryEntry may inform current-state interpretation, but is not current state by default.
FarmMemoryRetrievalQualification must be visible where farm memory materially affects high-consequence outputs.
Invalidated or expired farm memory must not drive high-consequence use without review.
Learning outputs must not update current state unless separately promoted through accepted OFARM pathways.
```

---

## 35. Interaction with CP11

CP13 must respect CP11.

Learning and experimentation may not optimise away hard sustainability constraints. A learning workflow involving sustainability-sensitive intervention, claim, metric, exception, risk budget, regret budget, or charter-sensitive output must link applicable CP11 gates.

CP13 may use CP11 `RiskBudget` and `RegretBudget` hooks, but these do not create experiment authority by themselves.

A learning result cannot:

- approve a CP11 charter exception;
- weaken a sustainability constraint;
- create sustainability claim basis;
- convert a charter breach into compliance fact;
- bypass CP11 output qualification;

unless normal CP11 gates explicitly support the use.

---

## 36. Interaction with CP12

CP13 may learn from CP12 mission records, but may not create mission authority.

An experiment or learning workflow involving physical operations must respect CP12 where cyber-physical mission execution is involved.

Rules:

```text
ExperimentProtocol is not MissionDispatchAuthorization.
TrialDesign is not MissionPlan.
TreatmentArm is not CommandEnvelope.
OutcomeObservationSet is not MissionVerification.
LearningEvaluationTrace is not dispatch authority.
FarmMemoryEntry is not a mission safety proof.
```

CP12 telemetry, receipts, verification, near-miss, and safety incidents may support learning evidence bundles only with provenance, scope, quality, and limitations.

---

## 37. Interaction with agents and capability manifests

Agents may participate in CP13 only through explicit authority.

Allowed under appropriate authority:

- propose hypotheses;
- prepare experiment protocol candidates;
- analyse evidence;
- generate outcome summaries;
- prepare causal estimate candidates;
- prepare farm-memory promotion packages;
- identify invalidation candidates;
- retrieve farm memory with qualification;
- produce advisory recommendations;
- request evidence.

Not allowed by default:

- approve experiment protocols;
- promote farm memory;
- invalidate farm memory;
- authorise training data use;
- share learning across farms;
- approve high-consequence farm-memory retrieval;
- deploy improved models or generated software;
- authorise physical missions;
- create compliance facts.

Capability manifests may describe CP13 support. They do not grant learning authority, farm-memory promotion authority, training-data permission, or deployment authority.

---

## 38. Interaction with future CP14 and CP15

### 38.1 CP14 deferral

CP13 is local/farm-scoped by default. It does not define cross-farm intelligence.

Deferred to CP14:

- farm-to-farm learning exchange;
- federated learning;
- cross-farm benchmarking;
- regional alerts;
- benchmark deltas;
- aggregation floors;
- re-identification risk;
- derivative model-use rights;
- commercial-use restrictions;
- regional/pool model updates;
- cross-farm data-sharing contracts for learning.

CP13 artifacts may include future CP14 eligibility markers, but they must not share, aggregate, or train cross-farm systems without CP14 authority.

### 38.2 CP15 deferral

CP13 does not define software or model deployment governance.

Deferred to CP15:

- generated software artifacts;
- generated adapters;
- model deployment;
- model registry/model card governance;
- training pipelines;
- canary rollout;
- rollback;
- SBOM/build provenance;
- deployment promotion;
- generated workflow deployment;
- robot adapter deployment.

A learning result may recommend model improvement. It cannot deploy it.

---

## 39. Machine-contract implications

If this RFC is accepted for implementation work, CP13 should create draft/non-default machine contracts before any current/default promotion.

Recommended first-wave contracts:

```text
LearningScope
LearningHypothesis
ExperimentProtocol
TrialDesign
ExperimentalUnit
TreatmentArm
ControlCondition
RandomizationPlan
BlockingFactor
OutcomeMeasureSpec
OutcomeObservationSet
LearningEvidenceBundle
LearningEvaluationTrace
CausalEstimate
LearningPromotionDecision
FarmMemoryEntry
FarmMemoryInvalidationRule
FarmMemoryRetrievalQualification
SeasonalLearningSummary
LearningOutputQualification
ExperimentRollbackTrigger
ExperimentException
```

Recommended staging path:

```text
03_machine_contracts/drafts_non_default/learning_experimentation_farm_memory/
```

Required currentness posture:

```text
CP13 machine contracts are draft/non-default until separately promoted.
CP13 must not promote CP11 or CP12 draft/non-default contracts to current/default.
```

Machine-contract design requirements:

- JSON Schema 2020-12;
- strict `additionalProperties: false` unless deliberately justified;
- draft/non-default `$id` and `schemaVersion` posture;
- explicit non-authorisation guardrails;
- explicit scope references;
- explicit authority/action references;
- explicit Advisory/Compliance posture;
- explicit current-state reliance posture;
- explicit CP11/CP12 reliance posture where material;
- explicit CP14/CP15 deferral posture;
- conditional validation for promotion, invalidation, retrieval, and high-consequence output states;
- conformance fixtures for positive and negative paths.

---

## 40. Conformance implications

CP13 requires executable conformance. A fixture plan alone is insufficient.

Minimum conformance families:

```text
learning_output_does_not_create_truth
experiment_protocol_does_not_authorise_operation
trial_design_does_not_authorise_mission
agent_memory_cannot_become_farm_memory
farm_memory_entry_requires_promotion_decision
farm_memory_retrieval_requires_qualification_for_high_consequence_use
causal_estimate_without_evidence_bundle_fails
causal_estimate_with_post_hoc_measure_requires_disclosure
learning_promotion_without_authority_fails
learning_promotion_without_scope_fails
invalidated_farm_memory_cannot_drive_high_consequence_recommendation
seasonal_summary_does_not_update_current_state
cp11_risk_budget_does_not_authorise_experiment
cp12_mission_receipt_does_not_create_learning_conclusion
mission_verification_can_support_learning_evidence_bundle
learning_output_cannot_authorise_model_deployment
learning_output_cannot_share_cross_farm_without_cp14
valid_local_strip_trial_learning_chain_passes
valid_farm_memory_promotion_with_review_passes
valid_retrieval_qualification_for_advisory_recommendation_passes
```

Conformance should test:

- schema validation;
- semantic hardening;
- cross-record consistency;
- authority gates;
- promotion gates;
- scope matching;
- invalidation rules;
- output qualification;
- CP11/CP12 interaction;
- CP14/CP15 deferral boundaries;
- positive and negative paths.

---

## 41. Migration notes

CP13 should not invalidate existing local-knowledge or planning artifacts.

Existing artifacts may map as follows:

| Existing artifact | CP13 posture |
|---|---|
| `LocalArtifact` | May remain local/supporting artifact; not automatically farm memory. |
| `NarrativeObservation` | May become evidence input; not farm memory by itself. |
| `LocalMemoryRule` | May be treated as predecessor/limited memory artifact; not full CP13 promoted farm memory unless migrated. |
| `PlannedIntervention` | May inform experiment/trial plan; not execution or mission authority. |
| `WorldModelRun` / `ScenarioResultSet` | Advisory evidence/model output; not causal truth. |
| `BridgeCandidate` | Candidate handoff from learning to next governed action. |
| CP11 `RiskBudget` / `RegretBudget` | Bounded hooks; not experiment authority. |
| CP12 mission telemetry/receipt/verification | Evidence candidates for learning; not learning conclusions. |

Migration should distinguish:

```text
legacy/local memory-like text
advisory observation
candidate farm memory
promoted farm memory
invalidated/superseded farm memory
```

No automatic bulk promotion of existing local notes or agent memories is permitted.

---

## 42. Readiness and non-claims

If accepted, CP13 may claim:

- bounded model-law support for learning, experimentation, causal-evidence, farm-memory, seasonal-learning, and learning-promotion governance;
- explicit separation of learning output, causal estimate, farm memory, agent memory, and truth/current-state/compliance/mission/deployment authority;
- draft/non-default machine-contract direction for CP13 artifacts once produced;
- conformance expectations for CP13 learning boundaries.

CP13 must not claim:

- production autonomous self-improvement readiness;
- production agronomic advice certification;
- automated experiment-authority readiness;
- autonomous model improvement or deployment readiness;
- farm-to-farm intelligence readiness;
- federated learning readiness;
- model/software deployment governance readiness;
- CP14 readiness;
- CP15 readiness;
- legal, certification, insurance, or regulatory advice;
- livestock-specific learning law;
- cross-farm validity of learning outputs;
- current/default CP13 machine-contract promotion before separate currentness promotion.

---

## 43. Risks and open questions

### 43.1 Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Farm memory becomes hidden current state | Existential | Require promotion decision, retrieval qualification, invalidation, and no-hidden-current-state rule. |
| Agent memory is confused with farm memory | High | Explicit agent/farm-memory separation and conformance fixtures. |
| Experiment result becomes automatic causal fact | High | Require causal-estimate and evaluation-trace rules. |
| Trial design authorises operations or missions | High | Explicit non-authorisation boundary; CP12 required for missions. |
| Outcome hacking creates fake learning | High | Require predeclared/post-hoc outcome disclosure. |
| Weak evidence supports strong farm memory | High | Evidence bundle, sufficiency, uncertainty, and promotion gates. |
| Farm-specific learning is generalized outside scope | High | LearningScope and retrieval qualification. |
| CP13 becomes CP14 by stealth | High | Local/farm-scoped default and cross-farm deferral. |
| CP13 becomes CP15 by stealth | High | Learning result may recommend model/software change but cannot deploy. |
| CP11 risk/regret budgets become experiment authority | High | Non-authorising integration rule. |
| CP12 mission records become causal conclusions | Medium/high | Treat mission records as evidence candidates only. |
| Farmer-facing learning outputs become noisy or overconfident | Medium/high | LearningOutputQualification and display policy. |

### 43.2 Open questions

Open questions for later phases:

1. Which minimum causal-estimate fields should be mandatory in machine contracts?
2. How strict should trial-design requirements be for low-resource farms and informal strip trials?
3. How should CP13 treat purely observational learning versus designed experiments?
4. What is the minimum viable farm-memory promotion workflow?
5. Which farm-memory retrieval uses are high-consequence by default?
6. Which local-memory predecessor artifacts should receive migration helpers?
7. How should CP13 expose uncertainty to farmers without creating noise?
8. Which CP13 concepts should remain companion-level examples rather than baseline law?
9. How should CP13 prepare, but not implement, CP14 cross-farm eligibility markers?
10. How should CP13 prepare, but not implement, CP15 model/software improvement recommendations?

---

## 44. Acceptance gate

CP13 is acceptable only if:

```text
[ ] The RFC preserves existing OFARM truth, current-state, Advisory/Compliance, authority, pack, output, CP11, and CP12 law.
[ ] The RFC does not create a third twin or hidden learning truth store.
[ ] The RFC keeps learning local/farm-scoped by default.
[ ] The RFC explicitly defers CP14 cross-farm intelligence.
[ ] The RFC explicitly defers CP15 model/software deployment.
[ ] Learning artifacts do not become truth by existence.
[ ] Experiment protocols do not authorise operations or missions.
[ ] Causal estimates do not become Compliance Twin facts by existence.
[ ] Farm memory entries require promotion, invalidation, and retrieval qualification law.
[ ] Agent memory remains separate from OFARM farm memory.
[ ] CP11 RiskBudget/RegretBudget integration remains non-authorising.
[ ] CP12 mission/operation records are evidence candidates only.
[ ] Machine contracts are staged draft/non-default.
[ ] Conformance includes positive and negative fixtures.
[ ] Readiness and non-claims remain explicit.
```

---

## 45. Phase 3 conclusion

This draft RFC establishes CP13 as the controlled amendment for **Learning, Experimentation, and Farm Memory**.

It should proceed to Phase 4 baseline patch planning only after architect review.

Phase 4 should produce controlled patch text for:

```text
00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md
00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md
00_active_baseline/OFARM_Alignment_Register_v0_13.md
00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md
00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md
```

Phase 4 must not create machine schemas and must not start CP14 or CP15.


---

## Phase 7 reconciliation and hardening note — 2026-05-29

This final CP13 RFC candidate reconciles the Phase 6 hostile review and Phase 6.1 remediation. The reconciliation adds the following acceptance constraints without changing CP13 scope:

1. `LearningEvaluationTrace` must not allow advisory or promotion dispositions when hard learning checks fail or are blocked.
2. `CausalEstimate` must keep causal strength, method, uncertainty, and review basis aligned; an insufficient method cannot carry directional or high-confidence effect claims.
3. `LearningPromotionDecision` must not promote farm memory without target, review, authority trace, effective period, and no current-state/compliance mutation.
4. `FarmMemoryEntry` must not be agent memory, hidden current state, or compliance fact; active farm memory requires a matching approved learning-promotion decision.
5. `LearningOutputQualification` must block current-state, compliance, mission-authority, model-deployment, cross-farm, unqualified-claim, and autonomous-self-improvement uses unless a later accepted gate allows them.
6. `OutcomeObservationSet` must expose material missingness, data quality, stale/invalidated evidence, and sufficiency limits.
7. `LearningScope` is Advisory by default; mixed or Compliance-bridged posture requires explicit bridge/review context.
8. `ExperimentException`, `ExperimentProtocol`, and `TrialDesign` do not authorise operations, missions, or model deployment.

CP13 does not promote CP11 or CP12 draft/non-default schemas, does not define CP14 farm-to-farm intelligence, and does not define CP15 generated-software/model-deployment law.
