# CP14 Phase 4 — Baseline Patch Plan

Date: 2026-05-29  
Status: controlled baseline patch plan  
Amendment: CP14 — Farm-to-Farm Intelligence Boundary  
Inputs: CP14 Phase 0 Source Proof, CP14 Phase 1 Scope Memo, CP14 Phase 2 Constitutional Issue Docket, CP14 Phase 3 RFC draft  
Output type: baseline patch plan only  

---

## 0. Phase 4 verdict

```text
CP14 should proceed to machine-contract planning after this phase.
Do not merge this patch yet.
Do not create CP14 schemas in this phase.
Do not start CP15 in this phase.
Do not promote CP11, CP12, CP13, or CP14 draft/non-default schemas to current/default.
```

CP14 is correctly scoped as:

```text
Farm-to-Farm Intelligence Boundary law
```

not:

```text
OFARM Social constitution
OFARM Exchange constitution
public benchmark product law
production federated-learning platform law
model/software deployment governance
generic reputation law
legal/certification/advice readiness
```

The baseline patch should add only the constitutional and runtime invariants needed to make cross-farm intelligence governable. Details belong in the CP14 RFC, companion policy, draft/non-default machine contracts, and conformance fixtures.

## 0.1 Core invariant to preserve

```text
Cross-farm intelligence is advisory by default.
Farm-to-farm sharing is not authority.
Aggregation is not anonymisation by assertion.
Regional alerts are not farm-level truth.
Benchmark deltas are not compliance facts.
Federated-learning contribution is not model deployment authority.
CP13 local learning may not cross farm boundaries without CP14 governance.
```

## 0.2 Existing law CP14 must not reopen

CP14 must not reopen:

```text
- assertion/history-first canonical truth;
- governed current-state materialisation;
- Advisory Twin / Compliance Twin separation;
- authority/default-deny law;
- pack/profile law;
- query/output qualification law;
- AI/agent actorship and run-trace law;
- CP11 sustainability charter law;
- CP12 cyber-physical mission law;
- CP13 local learning, experimentation, and farm-memory law.
```

## 0.3 Baseline patch summary

| Baseline file | Patch posture | Baseline now? | Details remain below baseline? |
|---|---:|---:|---:|
| `OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md` | append CP14 baseline addendum | yes | yes, RFC/contracts/conformance |
| `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md` | append CP14 runtime addendum and gate placement | yes | yes |
| `OFARM_Alignment_Register_v0_13.md` | add CP14 concepts and addendum | yes | no, register only |
| `OFARM_post_gap_closure_readiness_gate_memo_v0_1.md` | append CP14 readiness/non-claim addendum | yes | stronger claims require evidence |
| `OFARM_final_hostile_review_after_gap_closure_v0_1.md` | append CP14 hostile-review update | yes | final hostile review after schemas/conformance may refine |

---

# 1. File: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`

## 1.1 Patch C14-C-1 — Add CP14 baseline addendum

### Exact section to add or amend

Append after the CP13 baseline addendum:

```text
## CP14 Farm-to-Farm Intelligence Boundary baseline addendum — 2026-05-29
```

### Proposed normative text

```text
## CP14 Farm-to-Farm Intelligence Boundary baseline addendum — 2026-05-29

Status: controlled baseline patch candidate for `OFARM_Farm_to_Farm_Intelligence_Boundary_RFC_v0_1.md`.

CP14 introduces a bounded farm-to-farm intelligence boundary layer into OFARM model law.

CP14 governs cross-farm sharing, received intelligence, regional alerts, benchmark deltas, aggregation/deidentification/anonymisation claims, re-identification-risk assessment, derivative-use restrictions, training-use restrictions, federated-learning contribution boundaries, contribution-quality review, poisoning/anomaly review, revocation propagation, and cross-farm intelligence-output qualification.

CP14 does not replace the Constitution, create a second truth model, alter assertion/history-first authority, promote received intelligence into farm truth, collapse Advisory and Compliance Twins, weaken CP11 sustainability disclosure law, weaken CP12 cyber-physical mission boundaries, weaken CP13 local farm-memory boundaries, or make software agents hidden cross-farm sharing governors.

The CP14 invariant is:

`Cross-farm intelligence is advisory by default. Farm-to-farm sharing is not authority. Aggregation is not anonymisation by assertion. Regional alerts are not farm-level truth. Benchmark deltas are not compliance facts. Federated-learning contribution is not model deployment authority. CP13 local learning may not cross farm boundaries without CP14 governance.`

A CP14 artifact may affect harder OFARM outcomes only through explicit authority, evidence, review, promotion, current-state, output, CP11, CP12, CP13, and later CP15 gates where applicable.

### CP14-C.1 Farm-to-farm intelligence purpose and boundary

CP14 applies to farm-intelligence-sensitive use where farm-scoped data, summaries, evidence, sustainability indicators, mission/incident signals, local learning artifacts, farm-memory derivatives, regional alerts, benchmark deltas, aggregates, deidentified/anonymised datasets, federated-learning contributions, model-improvement signals, or received cross-farm intelligence materially affect recommendation, planning, warning, output, disclosure, claim, sharing, benchmark, model-improvement, or high-consequence reliance.

CP14 applies to crop-farming OFARM contexts already within the active baseline scope. It does not expand OFARM into livestock-specific cross-farm intelligence, animal-health intelligence, welfare intelligence, herd/flock intelligence, veterinary signal exchange, or public social-network law.

CP14 is not OFARM Social, OFARM Exchange, a public benchmark product, production federated-learning platform law, generated-software/model-deployment law, generic reputation law, or legal/certification/advice readiness.

### CP14-C.2 CP14 core concepts

The following CP14 concepts are baseline-recognised OFARM-governed concepts and must be represented in the Alignment Register before they are treated as constitutional core:

- `FarmIntelligenceBoundary`;
- `FarmIntelligenceSharePolicy`;
- `FarmIntelligenceShareGrant`;
- `FarmIntelligenceContribution`;
- `IntelligenceContributionPackage`;
- `LearningArtifactSharePackage`;
- `RecipientUseConstraint`;
- `DerivativeUsePolicy`;
- `TrainingUsePolicyBinding`;
- `RevocationPropagationTrace`;
- `RegionalAlert`;
- `RegionalRiskSignal`;
- `RegionalAlertCorrection`;
- `RegionalAlertWithdrawal`;
- `BenchmarkDelta`;
- `AggregationFloor`;
- `DeidentificationClaim`;
- `AnonymisationClaim`;
- `ReidentificationRiskAssessment`;
- `FederatedLearningContribution`;
- `FederatedAggregationReceipt`;
- `ModelImprovementSignal`;
- `TrainingUseReceipt`;
- `ContributionQualityAssessment`;
- `PoisoningOrAnomalyReview`;
- `CrossFarmApplicabilityAssessment`;
- `IntelligenceOutputQualification`.

These concepts may be detailed by accepted RFCs, companion artifacts, draft/non-default machine contracts, and conformance fixtures. They may not be introduced silently through an app, dashboard, pack, adapter, AI memory, cross-farm exchange payload, data-space import, buyer programme, federated-learning service, public benchmark, social feature, or sister platform.

### CP14-C.3 Cross-farm Advisory-default rule

Received cross-farm intelligence belongs to the Advisory Twin by default.

A `RegionalAlert`, `RegionalRiskSignal`, `BenchmarkDelta`, `FarmIntelligenceContribution`, `LearningArtifactSharePackage`, `FederatedAggregationReceipt`, `ModelImprovementSignal`, or other received intelligence artifact may raise risk flags, request observation, suggest review, inform advisory planning, qualify an output, or trigger a CP14-governed applicability assessment.

It may not directly create:

- farm-level occurrence truth;
- farm-level current state;
- Compliance Twin fact;
- accepted execution consequence;
- accepted CP11 sustainability claim;
- CP12 mission dispatch authority;
- CP13 farm-memory entry;
- CP15 model/software deployment authority;
- public benchmark claim;
- legal/certification/insurance conclusion.

A bridge from cross-farm intelligence toward harder OFARM consequences must pass ordinary OFARM authority, evidence, current-state, review, promotion, CP11, CP12, CP13, output, and later CP15 gates where applicable.

### CP14-C.4 Sharing and recipient-use law

Farm-to-farm sharing is a governed disclosure and use event. It is not authority to assert, review, decide, attest, file, promote, deploy, or operate.

A `FarmIntelligenceShareGrant` or equivalent CP14-governed share authorization must declare scope, source farm or contribution scope, recipient class, permitted purposes, prohibited purposes, retention posture, onward-sharing posture, derivative-use posture, training-use posture, revocation posture, redaction/aggregation/deidentification/anonymisation posture, and output-use limits.

A `RecipientUseConstraint` binds the recipient-side use of shared intelligence. A recipient may not expand received intelligence beyond declared purpose, scope, retention, derivative-use, training-use, onward-sharing, or output constraints merely because the payload is technically accessible.

A `DerivativeUsePolicy` governs whether derived features, summaries, benchmarks, model-improvement signals, embeddings, transformed datasets, aggregates, or downstream outputs may be created. Derivative use is not automatically allowed by sharing.

A `TrainingUsePolicyBinding` governs whether shared intelligence may train, fine-tune, evaluate, benchmark, or improve models. Training use is not automatically allowed by sharing, aggregation, deidentification, or platform access.

A `RevocationPropagationTrace` is required when a share grant, derivative-use permission, training-use permission, alert, benchmark, or intelligence package is revoked, narrowed, corrected, withdrawn, disputed, or invalidated in a way that materially affects downstream use.

### CP14-C.5 CP13 local learning and farm memory crossing boundary

CP13 local learning and farm memory are farm-scoped by default. A CP13 `FarmMemoryEntry`, `SeasonalLearningSummary`, `CausalEstimate`, `LearningEvaluationTrace`, `LearningEvidenceBundle`, or `LearningPromotionDecision` must not cross a farm boundary as shareable intelligence unless governed by CP14.

A `LearningArtifactSharePackage` must preserve scope, evidence basis, uncertainty, missingness, bias, limitations, invalidation posture, retrieval qualification, prohibited uses, and source-farm disclosure policy.

A received CP13-derived learning artifact remains Advisory by default and must not become local farm memory, current state, claim basis, mission authority, Compliance Twin fact, or model deployment authority without applicable OFARM gates.

### CP14-C.6 Regional alerts, risk signals, and applicability

A `RegionalAlert` or `RegionalRiskSignal` is not farm-level occurrence truth.

A regional pest, disease, weather, input, safety, sustainability, mission, or incident signal may indicate a regional risk context. It must not be treated as evidence that the same event, condition, infestation, disease, contamination, breach, mission incident, or risk exists on a particular farm without local evidence or a governed `CrossFarmApplicabilityAssessment`.

A `CrossFarmApplicabilityAssessment` must declare scope match, context similarity, evidence transferability, uncertainty, limitations, missing local evidence, and prohibited uses.

A `RegionalAlertCorrection` or `RegionalAlertWithdrawal` must propagate to materially affected downstream outputs, alerts, benchmark deltas, applicability assessments, agent runs, and query results where required by policy.

### CP14-C.7 Benchmark delta and public benchmark boundary

A `BenchmarkDelta` is not compliance fact, certification status, economic advice, legal conclusion, public ranking, or farm-performance truth by itself.

Benchmark outputs must declare cohort definition, aggregation floor, inclusion/exclusion criteria, data-quality posture, missingness, sample size class, re-identification risk, uncertainty, normalisation method, allowed uses, prohibited uses, and disclosure posture.

Public benchmark products, leaderboards, marketplace ratings, social reputation, or buyer-facing ranking systems are not created by CP14. They require separate product/sister-platform governance.

### CP14-C.8 Aggregation, deidentification, anonymisation, and re-identification risk

Aggregation is not anonymisation by assertion.

A `DeidentificationClaim` states a governed reduction of directly identifying detail. It does not claim irreversible anonymity unless separately supported.

An `AnonymisationClaim` requires explicit method basis, aggregation floor, residual-risk posture, re-identification-risk assessment, context limitation, and intended-use limitation. It must not be inferred merely from removal of names or farm identifiers.

A `ReidentificationRiskAssessment` is required where shared, published, partner-facing, or model-training uses rely on deidentification, anonymisation, aggregation, redaction, or cohorting to protect farm identity or commercial confidentiality.

### CP14-C.9 Federated-learning and model-improvement boundary

A `FederatedLearningContribution` is a governed contribution to a learning or aggregation process. It is not model deployment authority, software deployment authority, truth, current state, Compliance Twin fact, CP13 farm memory, or claim basis by itself.

A `FederatedAggregationReceipt` records aggregation or receipt posture. It is not proof that the resulting model is valid, safe, unbiased, deployable, authorised, or production-ready.

A `ModelImprovementSignal` may indicate that a model, heuristic, threshold, feature, benchmark, or candidate update may deserve review. It is not authority to deploy, fine-tune, update, activate, or promote a model or generated software artifact.

A `TrainingUseReceipt` records that a permitted training or evaluation use occurred under a declared policy. It does not expand future training, derivative, deployment, or sharing rights.

Model/software deployment governance belongs to CP15.

### CP14-C.10 Contribution quality, poisoning, and anomaly review

A `ContributionQualityAssessment` must qualify cross-farm intelligence by source trust posture, evidence quality, missingness, freshness, scope fit, method basis, uncertainty, anomaly posture, poisoning risk, and known limitations where relevant.

A `PoisoningOrAnomalyReview` is required when received intelligence, aggregate data, federated contributions, regional alerts, or benchmark deltas appear malicious, inconsistent, out-of-distribution, adversarial, contaminated, fabricated, commercially manipulated, or otherwise unsafe for reliance.

A poisoning or anomaly review may block, quarantine, downgrade, require review, require local confirmation, or mark downstream outputs as limited. It does not create Compliance Twin fact or blame/liability determination by itself.

### CP14-C.11 CP11, CP12, and sustainability/mission disclosure interaction

CP11 sustainability outputs, evidence, metrics, claim bases, charter breaches, exceptions, or risk budgets may not become cross-farm intelligence without CP14 disclosure and recipient-use governance.

CP12 mission telemetry, execution receipts, mission verification, near-miss events, physical safety incidents, emergency-stop activations, or mission safety records may not become cross-farm intelligence without CP14 disclosure, redaction, aggregation, re-identification-risk, recipient-use, and incident-sensitivity controls.

A CP14 output must preserve the original CP11/CP12/CP13 limitations, output qualifications, evidence posture, authority posture, and prohibited uses where material.

### CP14-C.12 Intelligence output qualification

A cross-farm intelligence output must carry an `IntelligenceOutputQualification` or equivalent result qualification when it is shared, received, displayed, exported, used by an agent, used in a query result, used in a benchmark, used in a regional alert, used in a model-improvement signal, or used in a high-consequence advisory context.

The qualification must disclose, where material:

- source type;
- sharing grant or lawful basis;
- recipient-use constraints;
- derivative-use and training-use posture;
- data-sovereignty boundary;
- aggregation/deidentification/anonymisation posture;
- re-identification-risk posture;
- contribution-quality posture;
- poisoning/anomaly-review posture;
- applicability assessment;
- Advisory-only status;
- output disposition;
- allowed and prohibited uses;
- uncertainty, missingness, evidence limitations, and correction/withdrawal status.

An intelligence output may not grant authority, create truth, create current state, create Compliance Twin fact, create claim basis, authorise missions, create farm memory, or deploy models by itself.

### CP14-C.13 Agent and tool-manifest boundary

A software agent may prepare, summarise, route, qualify, compare, or request review of cross-farm intelligence only within its authority envelope and applicable sharing/use constraints.

A software agent may not by default expand sharing, approve recipient use, approve derivative use, approve training use, override revocation, downgrade re-identification risk, treat received intelligence as local truth, promote regional signals to Compliance Twin fact, publish benchmarks, or deploy models.

Agent memory, model context, embeddings, vector stores, tool outputs, and generated summaries are not CP14 share grants, recipient-use approvals, training-use permissions, anonymisation claims, applicability assessments, or truth.

### CP14-C.14 Authority actions

CP14 adds farm-intelligence-sensitive action classes that must be evaluated under ordinary OFARM authority law, default deny, delegation, sharing, revocation, data sovereignty, and agent actorship rules.

The following action classes are baseline-recognised candidates for CP14 mapping in the Authority Action Matrix:

- `INTELLIGENCE_PREPARE_CONTRIBUTION`;
- `INTELLIGENCE_APPROVE_SHARE_GRANT`;
- `INTELLIGENCE_REVOKE_SHARE_GRANT`;
- `INTELLIGENCE_APPROVE_RECIPIENT_USE`;
- `INTELLIGENCE_APPROVE_DERIVATIVE_USE`;
- `INTELLIGENCE_APPROVE_TRAINING_USE`;
- `INTELLIGENCE_RECORD_TRAINING_USE`;
- `INTELLIGENCE_CREATE_REGIONAL_ALERT`;
- `INTELLIGENCE_CORRECT_OR_WITHDRAW_ALERT`;
- `INTELLIGENCE_CREATE_BENCHMARK_DELTA`;
- `INTELLIGENCE_APPROVE_PUBLIC_OR_PARTNER_BENCHMARK_OUTPUT`;
- `INTELLIGENCE_APPROVE_DEIDENTIFICATION_CLAIM`;
- `INTELLIGENCE_APPROVE_ANONYMISATION_CLAIM`;
- `INTELLIGENCE_ACCEPT_REIDENTIFICATION_RISK_ASSESSMENT`;
- `INTELLIGENCE_ACCEPT_FEDERATED_CONTRIBUTION`;
- `INTELLIGENCE_RECORD_FEDERATED_AGGREGATION_RECEIPT`;
- `INTELLIGENCE_CREATE_MODEL_IMPROVEMENT_SIGNAL`;
- `INTELLIGENCE_ACCEPT_POISONING_OR_ANOMALY_REVIEW`;
- `INTELLIGENCE_APPLY_REVOCATION_PROPAGATION`.

High-consequence CP14 action classes are human-governed or human-approval-required by default unless a later accepted RFC explicitly narrows that posture for a lower-risk class.

### CP14-C.15 Pack/profile surface law

CP14 permits pack/profile surfaces for farm-intelligence governance only where they do not mutate core OFARM meaning.

CP14 pack/profile surfaces may include sharing policy, recipient-use policy, derivative-use policy, training-use policy, aggregation floor, deidentification/anonymisation method profile, re-identification-risk threshold, regional-alert policy, benchmark-delta policy, contribution-quality policy, poisoning/anomaly-review policy, and intelligence-output qualification policy.

Packs must not weaken farm data sovereignty, sharing/revocation law, recipient-use constraints, CP11 claim limitations, CP12 mission/incident disclosure controls, CP13 farm-memory locality, or cross-farm Advisory-default posture without explicit governance.

### CP14-C.16 Conformance baseline

A conforming CP14 implementation must demonstrate, at minimum, that:

- received cross-farm intelligence remains Advisory by default;
- a regional alert does not create farm-level occurrence truth;
- a benchmark delta does not create compliance fact;
- a share package without a valid FarmIntelligenceShareGrant fails;
- recipient-use constraints block prohibited downstream use;
- derivative-use and training-use require explicit permission;
- revocation propagation blocks or qualifies materially affected downstream use;
- aggregation does not imply anonymisation;
- anonymisation claims require re-identification-risk assessment;
- public/partner benchmark outputs require aggregation floor and output qualification;
- CP13 local farm memory cannot cross farm boundaries without CP14 governance;
- federated-learning contribution does not authorise model deployment;
- model-improvement signal does not authorise model/software deployment;
- poisoning/anomaly review can quarantine or downgrade suspect intelligence;
- CP11 sustainability and CP12 mission/incident intelligence preserve their original limitations and disclosure controls;
- agents cannot approve sharing, derivative use, training use, benchmark publication, anonymisation claims, or model deployment by default.
```

### Reason

The Constitution needs a visible CP14 boundary because cross-farm intelligence is the next high-risk post-CP13 layer. Without baseline law, farm-to-farm signals can become hidden truth, authority, compliance facts, model-deployment pressure, or coercive disclosure.

### Interaction with existing law

This patch is additive. It reuses existing truth, authority, sharing, revocation, data-sovereignty, pack, query/output, CP11, CP12, and CP13 law.

### Risk of contradiction

Medium if CP14 language is interpreted as platform/product law for OFARM Social, Exchange, public benchmarks, or production federated learning. Mitigation: strong non-goals and Advisory-default boundary.

### Baseline or RFC?

The invariant, boundary, and concept recognition belong in baseline. Detailed contract fields, event grammar, pack merge rules, conformance fixtures, and examples remain in RFC/machine-contract/conformance layers.

### Migration note

Existing sharing grants and exchange starter contracts remain valid under their original scope. They do not become CP14 farm-intelligence share grants unless explicitly mapped.

### Conformance implication

CP14 conformance must test both outbound sharing and received-intelligence reliance, including negative tests for truth/authority/claim/deployment shortcuts.

---

## 1.2 Patch C14-C-2 — Add CP14 glossary entries

### Exact section to add or amend

Append to the Constitution glossary after CP13 glossary additions.

### Proposed normative text

```text
### FarmIntelligenceBoundary
A governed boundary for cross-farm intelligence sharing, receiving, output, qualification, revocation, derivative use, training use, benchmarking, regional alerts, federated contributions, and applicability assessment.

### FarmIntelligenceShareGrant
A governed grant authorising a defined farm-intelligence sharing scope, recipient class, purpose, retention posture, recipient-use constraints, derivative-use posture, training-use posture, revocation posture, and disclosure limits.

### FarmIntelligenceContribution
A bounded contribution of farm-scoped or farm-derived information into a cross-farm intelligence context.

### IntelligenceContributionPackage
A governed package containing one or more farm-intelligence contributions plus basis, scope, limitations, permitted uses, prohibited uses, and output qualifications.

### LearningArtifactSharePackage
A CP14-governed package for sharing CP13 learning artifacts, preserving scope, evidence, uncertainty, invalidation, retrieval qualification, and prohibited uses.

### RecipientUseConstraint
A governed constraint limiting how a recipient may use, retain, transform, onward-share, disclose, derive from, or train on shared intelligence.

### DerivativeUsePolicy
A governed policy controlling creation and use of derived features, summaries, embeddings, transformed datasets, benchmarks, model-improvement signals, or other derivative outputs.

### TrainingUsePolicyBinding
A governed binding controlling whether shared intelligence may be used for model training, fine-tuning, evaluation, benchmarking, or improvement.

### RevocationPropagationTrace
A trace showing how revocation, withdrawal, correction, narrowing, dispute, or invalidation of shared intelligence propagated to downstream recipients, outputs, artifacts, or uses.

### RegionalAlert
A regional advisory signal or warning that does not by itself establish farm-level occurrence truth.

### RegionalRiskSignal
A regional advisory risk signal that may inform observation, review, or local applicability assessment.

### BenchmarkDelta
A qualified comparison or difference between a farm, field, crop-cycle, metric, practice, cohort, or aggregate and a declared benchmark context. It is not compliance fact by itself.

### AggregationFloor
A governed minimum cohort, spatial, temporal, contribution-count, diversity, or disclosure-safety threshold required before aggregate intelligence may be disclosed or used.

### DeidentificationClaim
A claim that certain direct identifiers or identifying features have been reduced, removed, transformed, or masked under a declared method. It is not irreversible anonymisation by itself.

### AnonymisationClaim
A stronger claim that information is anonymised for a declared context and use, requiring method basis, aggregation floor, residual-risk posture, and re-identification-risk assessment.

### ReidentificationRiskAssessment
A governed assessment of the risk that a farm, party, field, practice, event, incident, or commercially sensitive pattern can be inferred from shared, aggregated, deidentified, anonymised, or derived intelligence.

### FederatedLearningContribution
A governed contribution to a federated or distributed learning process. It is not model deployment authority.

### FederatedAggregationReceipt
A receipt that a federated or distributed aggregation process accepted, rejected, transformed, or used a contribution under a declared policy. It is not model deployment evidence by itself.

### ModelImprovementSignal
An advisory signal that a model, heuristic, threshold, benchmark, feature, or candidate update may deserve review. It is not deployment authority.

### TrainingUseReceipt
A trace that shared intelligence was used for permitted training, fine-tuning, evaluation, benchmarking, or model-improvement use under a declared policy.

### ContributionQualityAssessment
A governed assessment of contribution quality, including provenance, freshness, missingness, evidence strength, scope fit, anomaly posture, poisoning risk, and limitations.

### PoisoningOrAnomalyReview
A governed review of suspected malicious, anomalous, fabricated, out-of-distribution, adversarial, commercially manipulated, or unsafe cross-farm intelligence.

### CrossFarmApplicabilityAssessment
A governed assessment of whether and how received intelligence may be relevant to a receiving farm or context, without becoming local truth by default.

### IntelligenceOutputQualification
A result qualification for cross-farm intelligence outputs, disclosing source, sharing authority, recipient-use constraints, derivative/training posture, aggregation/deidentification/anonymisation posture, re-identification risk, Advisory-only status, allowed uses, prohibited uses, uncertainty, limitations, correction, withdrawal, and revocation status.
```

### Reason

The Constitution must provide stable terms for the CP14 concept family.

### Interaction with existing law

No conflict if these entries remain boundary definitions and not full contract definitions.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline glossary entries should be concise. Contract details remain RFC/machine-contract law.

### Migration note

Use the exact names consistently across RFC, schemas, examples, conformance, and alignment register.

### Conformance implication

Schema names and conformance fixture names should align with these glossary names.

---

# 2. File: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`

## 2.1 Patch C14-P-1 — Add CP14 runtime gate

### Exact section to add or amend

Append after the CP13 runtime addendum or insert into the EnforcementChain section as a CP14 gate.

### Proposed normative text

```text
## CP14 Farm-to-Farm Intelligence Boundary runtime addendum — 2026-05-29

Status: controlled runtime patch candidate for `OFARM_Farm_to_Farm_Intelligence_Boundary_RFC_v0_1.md`.

CP14 adds a runtime boundary gate for farm-intelligence-sensitive use.

For outbound farm-to-farm intelligence sharing, the platform must resolve:

- data sovereignty boundary;
- sharing grant or lawful/authority basis;
- source farm or contribution scope;
- recipient class;
- permitted purposes;
- prohibited purposes;
- retention posture;
- onward-sharing posture;
- derivative-use posture;
- training-use posture;
- revocation posture;
- redaction/aggregation/deidentification/anonymisation posture;
- re-identification-risk posture where applicable;
- CP11/CP12/CP13 source limitations where material;
- intelligence-output qualification.

For received cross-farm intelligence, the platform must resolve:

- source and provenance posture;
- contribution quality;
- sharing/recipient-use constraints;
- derivative/training-use permissions;
- re-identification and disclosure limits;
- correction, withdrawal, revocation, dispute, poisoning, or anomaly posture;
- cross-farm applicability assessment where local reliance is contemplated;
- Advisory Twin posture by default;
- output and query qualification.

The CP14 gate must prevent received intelligence, regional alerts, benchmark deltas, aggregates, deidentified/anonymised payloads, federated receipts, model-improvement signals, or AI-generated cross-farm summaries from becoming local farm truth, current state, Compliance Twin fact, claim basis, mission authority, farm memory, model deployment authority, or public benchmark authority by default.
```

### Reason

The Platform Runtime must provide a gate for both outbound sharing and received-intelligence reliance.

### Interaction with existing law

This extends runtime enforcement without changing canonical truth, authority, current-state, CP11, CP12, or CP13 laws.

### Risk of contradiction

Medium if CP14 runtime gate is implemented as a general exchange platform. Mitigation: keep it boundary-only.

### Baseline or RFC?

Runtime gate belongs in baseline. Field-level details belong in CP14 RFC and machine contracts.

### Migration note

Existing exchange/import/share flows should be treated as non-CP14 farm-intelligence flows unless mapped into CP14 use classes.

### Conformance implication

CP14 conformance must verify outbound share gating, received-intelligence Advisory default, and blocked use of received intelligence as truth/authority.

---

## 2.2 Patch C14-P-2 — Add received-intelligence current-state boundary

### Exact section to add or amend

Insert after current-state/materialisation runtime sections or append in CP14 runtime addendum.

### Proposed normative text

```text
### CP14 received-intelligence current-state boundary

Received cross-farm intelligence is not current state.

A `RegionalAlert`, `RegionalRiskSignal`, `BenchmarkDelta`, `FarmIntelligenceContribution`, `LearningArtifactSharePackage`, `FederatedAggregationReceipt`, `ModelImprovementSignal`, `TrainingUseReceipt`, aggregate output, deidentified dataset, anonymised dataset, or AI-generated cross-farm intelligence summary must not update local farm current-state materialisation merely by being received, displayed, queried, or processed.

Where received intelligence materially informs a local recommendation, observation request, review package, BridgeCandidate, CP11 evaluation, CP12 mission preparation, CP13 learning evaluation, or output, the result must preserve the received-intelligence qualification and must not represent received intelligence as local truth unless separately established through OFARM truth and review law.
```

### Reason

Prevents regional or peer signals from becoming hidden current state.

### Interaction with existing law

Specialises existing current-state materialisation law for cross-farm intelligence.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline runtime law.

### Migration note

Received alerts and benchmarks should be migrated as Advisory inputs, not current-state facts.

### Conformance implication

Fixtures should test that regional alerts and benchmark deltas do not create farm-level current-state facts.

---

## 2.3 Patch C14-P-3 — Add CP14 AI/agent runtime boundary

### Exact section to add or amend

Append to AI/agent runtime addenda.

### Proposed normative text

```text
### CP14 agent-mediated cross-farm intelligence boundary

Software agents may prepare, summarise, qualify, route, compare, request review of, or produce advisory interpretations of farm-to-farm intelligence only under explicit authority, active sharing/use constraints, and CP14 output qualification.

Software agents may not by default:

- approve a FarmIntelligenceShareGrant;
- approve recipient-use expansion;
- approve derivative use;
- approve training use;
- override revocation;
- downgrade re-identification risk;
- approve anonymisation claims;
- publish partner/public benchmark outputs;
- convert received intelligence into local truth;
- create Compliance Twin facts;
- create CP13 farm memory from received intelligence;
- authorise CP12 missions;
- deploy or update models/software.

Agent memory, prompt context, embeddings, vector stores, tool results, retrieval results, generated summaries, or model-improvement signals are not CP14 authority, sharing grants, training-use permissions, anonymisation proof, applicability proof, or truth.
```

### Reason

Prevents agents from becoming hidden cross-farm intelligence governors.

### Interaction with existing law

Specialises existing agent actorship/tool-success boundaries.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline runtime boundary. Detailed action-class matrix belongs in RFC/addendum.

### Migration note

AI cross-farm summaries should be qualified as Advisory unless backed by CP14 gates.

### Conformance implication

Fixtures should test agent cannot approve share, derivative, training, anonymisation, public benchmark, or model deployment by default.

---

## 2.4 Patch C14-P-4 — Add CP14 output/query runtime rule

### Exact section to add or amend

Append after output/query runtime surfaces or CP13 output rules.

### Proposed normative text

```text
### CP14 intelligence output and query qualification

A query result, dashboard, API response, agent answer, exported file, PassportView, DocumentAssembly, regional alert, benchmark output, model-improvement signal, data-space payload, or partner/public-facing report that contains or materially relies on cross-farm intelligence must carry IntelligenceOutputQualification or an equivalent result qualification.

The qualification must expose Advisory-only status, source type, sharing grant or lawful basis, recipient-use constraints, derivative-use posture, training-use posture, re-identification-risk posture, aggregation/deidentification/anonymisation posture, applicability assessment, uncertainty, limitations, correction/withdrawal/revocation status, and allowed/prohibited downstream uses where material.

An intelligence output must not silently become truth, current state, Compliance Twin fact, claim basis, dispatch authority, farm memory, public benchmark authority, or model deployment authority.
```

### Reason

Prevents cross-farm intelligence from being over-read through outputs.

### Interaction with existing law

Specialises existing QuerySpecification/ResultQualification/PassportView/DocumentAssembly law.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline runtime law. Detailed qualification fields belong in CP14 schemas.

### Migration note

Existing cross-farm dashboards or reports should be qualified as Advisory unless CP14 claim/use basis exists.

### Conformance implication

Fixtures should test intelligence outputs cannot claim farm-level truth, compliance facts, public benchmark authority, or model deployment authority.

---

# 3. File: `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

## 3.1 Patch C14-A-1 — Add CP14 concepts to register

### Exact section to add or amend

Add rows to the Alignment Register concept table.

### Proposed register rows

```text
| FarmIntelligenceBoundary | Governance / Cross-farm intelligence | OFARM_OWNED | Data-space / interoperability standards as anchors only | OFARM uses “FarmIntelligenceBoundary” | OFARM needs a governed boundary for cross-farm intelligence sharing, receiving, output, revocation, derivative use, training use, benchmarks, regional alerts, and applicability. |
| FarmIntelligenceSharePolicy | Governance / Sharing | OFARM_OWNED | Existing sharing/data-sovereignty law as foundation | OFARM uses “FarmIntelligenceSharePolicy” | OFARM needs policy describing permitted farm-intelligence sharing contexts. |
| FarmIntelligenceShareGrant | Authority / Sharing | OFARM_OWNED | Existing SharingGrant as foundation | OFARM uses “FarmIntelligenceShareGrant” | OFARM needs a specialised grant for intelligence sharing, recipient use, derivative use, training use, retention, onward-sharing, and revocation. |
| FarmIntelligenceContribution | Cross-farm intelligence | OFARM_OWNED | External payload standards as mappings only | OFARM uses “FarmIntelligenceContribution” | OFARM needs bounded contribution records for farm-derived intelligence without treating them as recipient truth. |
| IntelligenceContributionPackage | Cross-farm intelligence / Packaging | OFARM_OWNED | Data-package standards as mappings only | OFARM uses “IntelligenceContributionPackage” | OFARM needs a governed package around contributions, use constraints, limitations, and output posture. |
| LearningArtifactSharePackage | CP13 / Cross-farm intelligence | OFARM_OWNED | None | OFARM uses “LearningArtifactSharePackage” | OFARM needs a CP14 boundary for sharing CP13 artifacts while preserving local scope, evidence, uncertainty, invalidation, and prohibited uses. |
| RecipientUseConstraint | Authority / Sharing / Use restriction | OFARM_OWNED | Contract/policy references as anchors only | OFARM uses “RecipientUseConstraint” | OFARM needs recipient-side use limits for shared intelligence. |
| DerivativeUsePolicy | Governance / Derived data | OFARM_OWNED | Data-license concepts as anchors only | OFARM uses “DerivativeUsePolicy” | OFARM needs derivative-use control separate from access. |
| TrainingUsePolicyBinding | Governance / Training use | OFARM_OWNED | ML/data-license concepts as anchors only | OFARM uses “TrainingUsePolicyBinding” | OFARM needs explicit model-training/evaluation/fine-tuning permission binding. |
| RevocationPropagationTrace | Governance / Revocation / Traceability | OFARM_OWNED | PROV-O foundations only | OFARM uses “RevocationPropagationTrace” | OFARM needs traceability for downstream effects of revoked, withdrawn, corrected, narrowed, or disputed intelligence. |
| RegionalAlert | Advisory intelligence | OFARM_OWNED | External alert systems as sources only | OFARM uses “RegionalAlert” | OFARM needs regional alerts that do not become farm-level truth by default. |
| RegionalRiskSignal | Advisory intelligence | OFARM_OWNED | External risk models as sources only | OFARM uses “RegionalRiskSignal” | OFARM needs regional risk signals that may prompt observation/review without creating truth. |
| RegionalAlertCorrection | Advisory intelligence / Correction | OFARM_OWNED | None | OFARM uses “RegionalAlertCorrection” | OFARM needs correction handling for regional alerts. |
| RegionalAlertWithdrawal | Advisory intelligence / Withdrawal | OFARM_OWNED | None | OFARM uses “RegionalAlertWithdrawal” | OFARM needs withdrawal handling for regional alerts. |
| BenchmarkDelta | Benchmark / Advisory intelligence | OFARM_OWNED | Benchmark standards as anchors only | OFARM uses “BenchmarkDelta” | OFARM needs benchmark deltas that do not become compliance fact or public ranking by default. |
| AggregationFloor | Disclosure / Privacy / Aggregation | OFARM_OWNED | Statistical disclosure control methods as anchors only | OFARM uses “AggregationFloor” | OFARM needs minimum aggregation thresholds for disclosure and benchmark safety. |
| DeidentificationClaim | Disclosure / Privacy | OFARM_OWNED | Privacy standards as anchors only | OFARM uses “DeidentificationClaim” | OFARM needs deidentification claims without implying irreversible anonymisation. |
| AnonymisationClaim | Disclosure / Privacy | OFARM_OWNED | Privacy standards as anchors only | OFARM uses “AnonymisationClaim” | OFARM needs stronger anonymisation claims with method and risk basis. |
| ReidentificationRiskAssessment | Disclosure / Privacy / Risk | OFARM_OWNED | Privacy-risk methods as anchors only | OFARM uses “ReidentificationRiskAssessment” | OFARM needs explicit residual re-identification-risk assessment for shared/aggregated/deidentified/anonymised intelligence. |
| FederatedLearningContribution | Learning / Cross-farm intelligence | OFARM_OWNED | Federated-learning frameworks as external implementations only | OFARM uses “FederatedLearningContribution” | OFARM needs governed federated-learning contributions without creating deployment authority. |
| FederatedAggregationReceipt | Learning / Cross-farm intelligence | OFARM_OWNED | Federated-learning frameworks as external implementations only | OFARM uses “FederatedAggregationReceipt” | OFARM needs receipt records for federated aggregation without creating model validity or deployment claims. |
| ModelImprovementSignal | Advisory / Model improvement | OFARM_OWNED | Model-card/model-registry concepts as anchors only | OFARM uses “ModelImprovementSignal” | OFARM needs model-improvement signals that do not authorise deployment. |
| TrainingUseReceipt | Traceability / Training use | OFARM_OWNED | ML governance concepts as anchors only | OFARM uses “TrainingUseReceipt” | OFARM needs trace of permitted training/evaluation use without expanding future rights. |
| ContributionQualityAssessment | Evidence / Quality / Cross-farm intelligence | OFARM_OWNED | Data-quality standards as anchors only | OFARM uses “ContributionQualityAssessment” | OFARM needs quality qualification for contributions. |
| PoisoningOrAnomalyReview | Security / Quality / Cross-farm intelligence | OFARM_OWNED | Security/anomaly methods as anchors only | OFARM uses “PoisoningOrAnomalyReview” | OFARM needs review of malicious, anomalous, contaminated, or unsafe cross-farm intelligence. |
| CrossFarmApplicabilityAssessment | Advisory / Applicability | OFARM_OWNED | None | OFARM uses “CrossFarmApplicabilityAssessment” | OFARM needs assessment of whether received intelligence applies locally without creating truth. |
| IntelligenceOutputQualification | Output / Cross-farm intelligence | OFARM_OWNED | Result-qualification foundations only | OFARM uses “IntelligenceOutputQualification” | OFARM needs qualification of cross-farm intelligence outputs, permitted uses, prohibited uses, limitations, sharing basis, and Advisory posture. |
```

### Reason

The Alignment Register must recognise CP14 concepts before they are constitutional core.

### Interaction with existing law

Additive. External data-space, privacy, benchmark, ML, and interoperability standards remain anchors or mappings, not hidden OFARM law.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline register update.

### Migration note

Use exact concept names in CP14 RFC, schemas, examples, conformance, and generated indexes.

### Conformance implication

Draft schemas should align with register names.

---

## 3.2 Patch C14-A-2 — Add CP14 alignment addendum

### Exact section to add or amend

Append after the CP13 alignment addendum.

### Proposed normative text

```text
## CP14 alignment register addendum — Farm-to-Farm Intelligence Boundary — 2026-05-29

Alignment item: CP14 Farm-to-Farm Intelligence Boundary controlled-promotion boundary.

Decision: CP14 promotes the farm-to-farm intelligence concept family as OFARM-owned governance/cross-farm-intelligence surfaces for intelligence-sensitive use.

The CP14 concept family aligns with active OFARM truth/current-state/twin/authority/pack/query/output, CP11, CP12, and CP13 boundaries by requiring cross-farm intelligence, sharing, recipient-use limits, derivative-use limits, training-use limits, revocation propagation, regional alerts, benchmark deltas, aggregation/deidentification/anonymisation claims, re-identification-risk assessment, federated-learning contributions, model-improvement signals, contribution-quality assessment, poisoning/anomaly review, applicability assessment, and intelligence-output qualification to remain explicit, traceable, and subordinate to existing OFARM law.

CP14 does not promote CP15 generated-software/model-deployment contracts, OFARM Social constitution, OFARM Exchange constitution, public benchmark product law, production federated-learning platform law, generic reputation law, or livestock-specific cross-farm intelligence law.

Residual debt: CP14 machine-contract schemas, conformance fixtures, privacy/legal review, external data-space review, federated-learning implementation evidence, public/partner benchmark product governance, farmer-facing comprehension evidence, and production/pilot validation remain outside baseline alignment until separately produced and reviewed.
```

### Reason

The register needs a CP14 currentness/alignment note.

### Interaction with existing law

No conflict.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline alignment register addendum.

### Migration note

CP14 concepts become aligned only after acceptance and baseline reconciliation.

### Conformance implication

Capability manifests should distinguish CP14 law from CP14 implementation readiness.

---

# 4. File: `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

## 4.1 Patch C14-R-1 — Add CP14 readiness addendum

### Exact section to add or amend

Append after the CP13 readiness addendum.

### Proposed normative text

```text
## CP14 Farm-to-Farm Intelligence Boundary readiness addendum — 2026-05-29

### Bounded continuation posture

CP14 improves OFARM by adding a governed boundary for farm-to-farm intelligence, sharing, received intelligence, regional alerts, benchmark deltas, deidentification/anonymisation claims, re-identification-risk assessment, federated-learning contribution boundaries, model-improvement signals, revocation propagation, contribution quality, poisoning/anomaly review, and intelligence-output qualification.

CP14 is a model/runtime governance closure, not a production farm-to-farm intelligence platform.

CP14 remains **implementation-directed with bounded debt** until the CP14 RFC, baseline patch, machine contracts, conformance fixtures, hostile review, implementation evidence, and steward validation are complete.

### Claims allowed after CP14 acceptance and reconciliation

After CP14 is accepted and reconciled, OFARM may claim:

- bounded model-law support for farm-to-farm intelligence boundaries;
- explicit Advisory-default posture for received cross-farm intelligence;
- explicit separation between sharing and authority;
- explicit boundaries for regional alerts, benchmark deltas, aggregation/deidentification/anonymisation claims, re-identification risk, derivative use, training use, federated contributions, and model-improvement signals;
- controlled hooks for CP15 model/software deployment governance without creating CP15 law;
- conformance-oriented posture for cross-farm intelligence output qualification and sharing/use restrictions.

### Claims still blocked after CP14

OFARM must not claim:

- production farm-to-farm intelligence platform readiness;
- production federated-learning platform readiness;
- public benchmark product readiness;
- OFARM Social readiness;
- OFARM Exchange readiness;
- legal/privacy/certification/insurance/advisory readiness;
- anonymisation guarantee;
- irreversible deidentification guarantee;
- regional-alert accuracy guarantee;
- benchmark fairness or public ranking readiness;
- model deployment readiness;
- generated-software deployment readiness;
- CP15 readiness;
- cross-farm intelligence as local farm truth;
- received intelligence as current state;
- benchmark delta as compliance fact;
- federated-learning contribution as deployment authority;
- current/default CP14 machine-contract promotion.

### Evidence required before stronger claims

Stronger CP14 claims require:

- accepted CP14 machine contracts;
- passing CP14 conformance fixtures;
- runtime evidence for share-grant enforcement;
- recipient-use, derivative-use, training-use, and revocation-propagation evidence;
- output qualification evidence;
- re-identification-risk and aggregation-floor validation;
- poisoning/anomaly-review evidence;
- CP13-to-CP14 learning-artifact share package tests;
- regional-alert correction/withdrawal tests;
- benchmark-delta cohort/aggregation tests;
- farmer-facing comprehension and burden validation;
- legal/privacy review where real personal/commercial data is involved;
- external data-space and sister-platform boundary review.
```

### Reason

CP14 could be overclaimed as privacy-safe, anonymised, federated-learning ready, or public benchmark ready. The readiness memo must block those claims.

### Interaction with existing law

Extends existing controlled-readiness posture.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline readiness posture.

### Migration note

CP14 acceptance should not imply production data-sharing readiness.

### Conformance implication

No stronger CP14 claim without conformance and runtime evidence.

---

# 5. File: `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

## 5.1 Patch C14-H-1 — Add CP14 hostile-review update

### Exact section to add or amend

Append after the CP13 hostile-review update.

### Proposed normative text

```text
## CP14 Farm-to-Farm Intelligence Boundary hostile-review update — 2026-05-29

A hostile reader should treat CP14 as a necessary farm-to-farm intelligence boundary extension, not as evidence that OFARM is now a production intelligence network, social platform, exchange platform, federated-learning platform, public benchmarking product, anonymisation engine, or model-deployment platform.

### Closed or substantially reduced

CP14 closes or reduces the following conceptual gaps:

- cross-farm intelligence is explicitly Advisory by default;
- farm-to-farm sharing is separated from authority;
- recipient-use, derivative-use, and training-use boundaries become explicit;
- revocation propagation becomes traceable;
- CP13 local learning and farm memory cannot cross farm boundaries without CP14 governance;
- regional alerts and risk signals cannot silently become farm-level truth;
- benchmark deltas cannot silently become compliance facts or public ranking authority;
- aggregation is not treated as anonymisation by assertion;
- deidentification and anonymisation claims require explicit method and risk basis;
- re-identification risk becomes a governed assessment surface;
- federated-learning contribution does not become model deployment authority;
- model-improvement signal does not become model/software deployment authority;
- contribution quality and poisoning/anomaly review become explicit;
- CP11 sustainability and CP12 mission/incident intelligence preserve source limitations when disclosed cross-farm;
- agents cannot approve sharing, derivative use, training use, anonymisation, public benchmark outputs, or model deployment by default.

### Still open and hostile-reader relevant

CP14 does not close:

- production farm-to-farm intelligence platform readiness;
- production federated-learning platform readiness;
- public benchmark product governance;
- OFARM Social constitution;
- OFARM Exchange constitution;
- CP15 generated-software/model-deployment governance;
- legal/privacy/certification/insurance/advisory readiness;
- real anonymisation guarantee;
- real-world re-identification-risk validation;
- external data-space integration readiness;
- benchmark fairness and cohort-design validation;
- farmer-facing comprehension and coercion-risk validation;
- production/pilot validation.

### Hostile-reader verdict

CP14 is the correct next extension if it remains a boundary amendment.

The main failure mode is not conceptual absence; it is overclaiming. Cross-farm intelligence can become coercive, commercially dangerous, privacy-invasive, or operationally misleading if Advisory-default, sovereignty, recipient-use, derivative-use, training-use, revocation, applicability, output qualification, and re-identification-risk gates are not mechanically enforced.

The correct post-CP14 posture remains:

**implementation-directed with bounded debt, not production-ready, not a social platform, not an exchange platform, not a public benchmark product, not federated-learning-platform ready, not anonymisation-guarantee ready, not model-deployment ready, and not CP15-ready.**
```

### Reason

The hostile-review file must frame CP14’s real contribution and residual risk.

### Interaction with existing law

No conflict.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline hostile-review posture.

### Migration note

Use this as Phase 6 hostile-review baseline after machine contracts exist.

### Conformance implication

Hostile review should require conformance tests for all listed closure claims.

---

# 6. CP14 RFC/addenda implications to carry forward

Phase 4 does not create these files yet, but Phase 7 should eventually produce or reconcile them:

```text
02_accepted_rfcs/OFARM_Farm_to_Farm_Intelligence_Boundary_RFC_v0_1.md
02_accepted_rfcs/addenda/OFARM_Authority_Action_Matrix_CP14_extension_v0_1.md
02_accepted_rfcs/addenda/OFARM_Event_Grammar_CP14_extension_v0_1.md
02_accepted_rfcs/addenda/OFARM_Pack_Merge_Semantics_CP14_surface_extension_v0_1.md
01_companion_artifacts/OFARM_Farm_to_Farm_Intelligence_Boundary_and_Data_Sovereignty_Policy_v0_1.md
```

## 6.1 Authority-action matrix extension candidates

CP14 authority-action mapping should include at least:

```text
INTELLIGENCE_PREPARE_CONTRIBUTION
INTELLIGENCE_APPROVE_SHARE_GRANT
INTELLIGENCE_REVOKE_SHARE_GRANT
INTELLIGENCE_APPROVE_RECIPIENT_USE
INTELLIGENCE_APPROVE_DERIVATIVE_USE
INTELLIGENCE_APPROVE_TRAINING_USE
INTELLIGENCE_RECORD_TRAINING_USE
INTELLIGENCE_CREATE_REGIONAL_ALERT
INTELLIGENCE_CORRECT_OR_WITHDRAW_ALERT
INTELLIGENCE_CREATE_BENCHMARK_DELTA
INTELLIGENCE_APPROVE_PUBLIC_OR_PARTNER_BENCHMARK_OUTPUT
INTELLIGENCE_APPROVE_DEIDENTIFICATION_CLAIM
INTELLIGENCE_APPROVE_ANONYMISATION_CLAIM
INTELLIGENCE_ACCEPT_REIDENTIFICATION_RISK_ASSESSMENT
INTELLIGENCE_ACCEPT_FEDERATED_CONTRIBUTION
INTELLIGENCE_RECORD_FEDERATED_AGGREGATION_RECEIPT
INTELLIGENCE_CREATE_MODEL_IMPROVEMENT_SIGNAL
INTELLIGENCE_ACCEPT_POISONING_OR_ANOMALY_REVIEW
INTELLIGENCE_APPLY_REVOCATION_PROPAGATION
```

Default posture should be human-governed or human-approval-required for high-consequence actions, especially share-grant approval, public/partner benchmark output, anonymisation claims, training use, derivative use, revocation override, and poisoning/anomaly acceptance.

## 6.2 Event grammar extension candidates

CP14 event grammar should include at least:

```text
FarmIntelligenceShareGrantRequested
FarmIntelligenceShareGrantApproved
FarmIntelligenceShareGrantRevoked
FarmIntelligenceContributionPackaged
IntelligenceContributionReceived
RecipientUseConstraintApplied
DerivativeUseApprovedOrDenied
TrainingUseApprovedOrDenied
TrainingUseRecorded
RevocationPropagationApplied
RegionalAlertIssued
RegionalAlertCorrected
RegionalAlertWithdrawn
BenchmarkDeltaCreated
AggregationFloorEvaluated
DeidentificationClaimCreated
AnonymisationClaimCreated
ReidentificationRiskAssessed
FederatedContributionSubmitted
FederatedAggregationReceiptRecorded
ModelImprovementSignalCreated
ContributionQualityAssessed
PoisoningOrAnomalyReviewOpened
PoisoningOrAnomalyReviewResolved
CrossFarmApplicabilityAssessed
IntelligenceOutputQualified
```

Events must not create local farm truth or Compliance Twin facts by existence alone.

## 6.3 Pack/profile surface candidates

CP14 pack/profile surfaces should include:

```text
FARM_INTELLIGENCE_SHARE_POLICY
RECIPIENT_USE_POLICY
DERIVATIVE_USE_POLICY
TRAINING_USE_POLICY
AGGREGATION_FLOOR_POLICY
DEIDENTIFICATION_METHOD_PROFILE
ANONYMISATION_METHOD_PROFILE
REIDENTIFICATION_RISK_POLICY
REGIONAL_ALERT_POLICY
BENCHMARK_DELTA_POLICY
CONTRIBUTION_QUALITY_POLICY
POISONING_ANOMALY_REVIEW_POLICY
INTELLIGENCE_OUTPUT_QUALIFICATION_POLICY
REVOCATION_PROPAGATION_POLICY
```

Merge defaults should be strongest requirement or hard fail for sovereignty, sharing, recipient-use, derivative-use, training-use, anonymisation, re-identification risk, revocation, public/partner output, and poisoning/anomaly review surfaces.

---

# 7. Candidate machine-contract implications for Phase 5

Phase 5 should produce draft/non-default contracts for:

```text
FarmIntelligenceBoundary
FarmIntelligenceSharePolicy
FarmIntelligenceShareGrant
FarmIntelligenceContribution
IntelligenceContributionPackage
LearningArtifactSharePackage
RecipientUseConstraint
DerivativeUsePolicy
TrainingUsePolicyBinding
RevocationPropagationTrace
RegionalAlert
RegionalRiskSignal
RegionalAlertCorrection
RegionalAlertWithdrawal
BenchmarkDelta
AggregationFloor
DeidentificationClaim
AnonymisationClaim
ReidentificationRiskAssessment
FederatedLearningContribution
FederatedAggregationReceipt
ModelImprovementSignal
TrainingUseReceipt
ContributionQualityAssessment
PoisoningOrAnomalyReview
CrossFarmApplicabilityAssessment
IntelligenceOutputQualification
```

Do not create CP15 deployment contracts. Do not create OFARM Social or Exchange contracts. Do not promote existing CP11/CP12/CP13 draft schemas.

---

# 8. Candidate conformance implications for Phase 5–7

Minimum conformance fixture families:

```text
received_regional_alert_does_not_create_farm_truth
benchmark_delta_does_not_create_compliance_fact
farm_intelligence_share_without_grant_fails
recipient_use_beyond_constraints_fails
derivative_use_without_policy_fails
training_use_without_policy_fails
revoked_share_blocks_downstream_use
aggregation_does_not_imply_anonymisation
anonymisation_claim_without_reid_risk_assessment_fails
public_benchmark_without_aggregation_floor_fails
cp13_farm_memory_cross_farm_without_cp14_package_fails
federated_contribution_does_not_authorise_model_deployment
model_improvement_signal_does_not_authorise_deployment
regional_alert_withdrawal_propagates_to_outputs
poisoned_contribution_is_quarantined
agent_cannot_approve_share_grant_by_default
agent_cannot_approve_training_use_by_default
agent_cannot_publish_benchmark_by_default
cp11_sustainability_claim_disclosure_requires_cp14_output_qualification
cp12_incident_signal_disclosure_requires_cp14_controls
valid_share_grant_with_recipient_constraints_passes
valid_regional_alert_advisory_display_passes
valid_benchmark_delta_with_aggregation_floor_passes
valid_federated_contribution_receipt_advisory_only_passes
```

---

# 9. Risks of the baseline patch

| Risk | Severity | Mitigation |
|---|---:|---|
| CP14 becomes OFARM Social or Exchange law | High | Strong non-goals and sister-platform boundary language |
| Received intelligence becomes farm truth | Existential | Advisory-default rule and current-state boundary |
| Sharing grant becomes authority grant | High | Explicit sharing-is-not-authority rule |
| Aggregation treated as anonymisation | High | Separate aggregation floor, deidentification, anonymisation, and re-identification assessment |
| Benchmark deltas become compliance/public ranking facts | High | Output qualification and benchmark non-claims |
| Federated contribution becomes model deployment authority | High | CP15 deferral and non-deployment rule |
| CP13 local farm memory leaks cross-farm | High | LearningArtifactSharePackage and CP14 crossing gate |
| Agents become hidden sharing/training governors | High | Agent action defaults and blocked high-governance actions |
| Buyer/certifier/cooperative coercion through intelligence outputs | High | recipient-use, display, burden, data-sovereignty, and public/partner output controls |
| CP14 overclaims privacy/anonymisation readiness | High | readiness non-claims and re-identification-risk gate |

---

# 10. Migration plan

Recommended migration order:

```text
1. Keep CP14 RFC as draft candidate until baseline patch, machine contracts, conformance, hostile review, and steward validation are complete.
2. Apply Constitution CP14 addendum only after RFC reconciliation.
3. Apply Platform Runtime CP14 addendum and gate placement.
4. Apply Alignment Register concept rows and CP14 addendum.
5. Apply readiness and hostile-review addenda.
6. Draft CP14 machine contracts under drafts_non_default only.
7. Build CP14 conformance runner and positive/negative fixtures.
8. Hostile-review CP14.
9. Remediate schemas/conformance.
10. Produce final CP14 package.
11. Merge only after repository steward validation passes.
```

---

# 11. Phase 4 conclusion

CP14 baseline patch should proceed as controlled addenda.

The patch is correctly bounded if it does only this:

```text
- makes farm-to-farm intelligence boundary visible in baseline law;
- makes cross-farm Advisory-default posture explicit;
- makes sharing not authority;
- separates aggregation, deidentification, anonymisation, and re-identification risk;
- prevents regional alerts and benchmarks from becoming farm truth/compliance facts;
- prevents federated-learning contributions and model-improvement signals from becoming deployment authority;
- preserves CP11, CP12, and CP13 limitations when their artifacts cross farm boundaries;
- adds CP14 concepts to the Alignment Register;
- adds runtime gate and output qualification posture;
- updates readiness and hostile-review non-claims;
- preserves all existing OFARM truth, current-state, authority, pack, output, agent, CP11, CP12, and CP13 law.
```

Recommended next command:

```text
Start CP14 Phase 5.

Create the CP14 machine-contract plan.

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
- relation to CP11 sustainability disclosure and claim basis;
- relation to CP12 mission/incident intelligence;
- relation to CP13 learning/farm-memory artifacts;
- relation to CP15 deferral;
- conformance tests;
- examples.

Then produce draft schema-style definitions in OFARM-compatible form.

Do not create generated-software or model-deployment contracts except as forward references to CP15.
Do not create OFARM Social, OFARM Exchange, public benchmark product, or generic reputation contracts.
Do not promote CP11, CP12, CP13, or CP14 draft/non-default schemas to current/default.
Do not claim production farm-to-farm intelligence or federated-learning readiness.
```
