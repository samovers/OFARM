# OFARM Farm-to-Farm Intelligence Boundary RFC v0.1

Date: 2026-05-29  
Status: accepted/merged CP14 RFC; active RFC law below the active baseline  
Target path: `02_accepted_rfcs/OFARM_Farm_to_Farm_Intelligence_Boundary_RFC_v0_1.md`  
Authority tier if accepted: accepted RFC; subordinate to `00_active_baseline/` and above companion artifacts under `PROJECT_AUTHORITY.md`  
Scope: introduce a bounded farm-to-farm intelligence boundary for cross-farm sharing, received intelligence, regional alerts, benchmark deltas, aggregation/deidentification claims, re-identification risk, derivative/training-use controls, federated contribution boundaries, revocation propagation, contribution quality, poisoning/anomaly review, and intelligence-output qualification without reopening OFARM truth, current-state, authority, pack, output, CP11, CP12, or CP13 law.

---

## 1. Purpose

OFARM already has a strong semantic and governance spine:

- assertion/history-first canonical truth;
- governed current-state materialisation;
- one semantic substrate with Compliance Twin and Advisory Twin partitions;
- explicit authority, delegation, sharing, revocation, and default-deny posture;
- data sovereignty boundaries, sharing grants, delegation grants, and revocation decisions;
- pack/profile law;
- query/output qualification and high-consequence output gates;
- sponsor-bound software-agent actorship;
- bounded agent run, trace, blocked-action, tool-manifest, and handoff law;
- Advisory-only world-model and scenario contracts;
- CP11 Sustainable Autonomous Farming Charter governance for sustainability-sensitive constraints, objectives, evidence, claims, exceptions, breaches, and output qualification;
- CP12 Cyber-Physical Mission Envelope governance for mission identity, preflight, dispatch, command integrity, safety envelope, telemetry, execution receipt, mission verification, and physical-safety incident boundaries;
- CP13 Learning, Experimentation, and Farm Memory governance for local hypotheses, experiments, causal estimates, learning promotion, farm memory, seasonal learning, and learning-output qualification.

That foundation is necessary but not sufficient for a farming platform where farms, cooperatives, regional services, advisors, processors, certifiers, buyers, AI agents, and other ecosystems exchange intelligence.

A future OFARM runtime may receive or share regional pest alerts, disease-pressure signals, benchmark deltas, local learning summaries, CP13 learning artifacts, CP11 sustainability indicators, CP12 mission/incident signals, federated-learning contributions, model-improvement signals, anonymised or deidentified aggregates, or partner-facing intelligence outputs. Without explicit cross-farm intelligence law, the platform can fail at a different high-consequence boundary:

```text
peer signal / regional alert / benchmark / shared learning package / federated receipt / AI summary
→ silently treated as local farm truth, authority, compliance fact, claim basis, or deployment permission
→ farm decisions, claims, missions, model updates, or disclosures depend on it
```

This RFC introduces the first CP14 contract layer for the **Farm-to-Farm Intelligence Boundary**.

The core decision is:

```text
Cross-farm intelligence is advisory by default.
Farm-to-farm sharing is not authority.
Aggregation is not anonymisation by assertion.
Regional alerts are not farm-level truth.
Benchmark deltas are not compliance facts.
Federated-learning contribution is not model deployment authority.
CP13 local learning may not cross farm boundaries without CP14 governance.
```

CP14 makes cross-farm intelligence governable. It does not create OFARM Social, OFARM Exchange, a production federated-learning platform, a public benchmarking product, or model/software deployment governance.

---

## 2. Scope

This RFC covers farm-to-farm intelligence boundary governance for crop-farming OFARM contexts already within the active baseline scope.

It defines:

- CP14 authority, scope, and non-goals;
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
- `CrossFarmApplicabilityAssessment`;
- `RegionalAlert`;
- `RegionalRiskSignal`;
- `RegionalAlertCorrection`;
- `RegionalAlertWithdrawal`;
- `BenchmarkDelta`;
- `AggregationFloor`;
- `DeidentificationClaim` and `AnonymisationClaim` posture;
- `ReidentificationRiskAssessment`;
- `FederatedLearningContribution`;
- `FederatedAggregationReceipt`;
- `ModelImprovementSignal`;
- `TrainingUseReceipt`;
- `ContributionQualityAssessment`;
- `PoisoningOrAnomalyReview`;
- `IntelligenceOutputQualification`;
- CP14 interaction with CP11 sustainability disclosure and claim-basis law;
- CP14 interaction with CP12 mission/incident intelligence boundaries;
- CP14 interaction with CP13 local learning and farm memory;
- CP14 authority actions;
- CP14 event grammar and commit-matrix implications;
- CP14 pack/profile surface implications;
- CP14 query/output gate implications;
- CP14 conformance implications;
- CP14 readiness and non-claims;
- explicit deferrals to CP15, OFARM Social, OFARM Exchange, public benchmark products, and future domains.

This RFC applies to **farm-intelligence-sensitive uses**, including:

- sharing farm-scoped data, summaries, alerts, learning artifacts, metrics, incidents, or benchmark information outside the farm boundary;
- receiving intelligence from another farm, cooperative, regional service, data space, buyer, supplier, advisor, certifier, platform, AI agent, or sister platform;
- producing regional alerts or regional risk signals;
- producing benchmark deltas or benchmark outputs;
- packaging CP13 learning artifacts for cross-farm sharing;
- using CP13 farm memory outside the originating farm context;
- using CP11 sustainability evidence, metrics, or claims in cross-farm intelligence;
- using CP12 mission telemetry, verification, near-miss, or physical-safety incident data in cross-farm intelligence;
- deidentifying, anonymising, aggregating, redacting, or transforming farm-scoped data;
- assessing re-identification risk;
- creating federated-learning contributions or aggregation receipts;
- creating model-improvement signals or training-use receipts;
- responding to revocation, withdrawal, correction, dispute, anomaly, poisoning, or misuse risk;
- agent-mediated cross-farm intelligence exchange;
- query/output surfaces that expose cross-farm intelligence.

---

## 3. Non-goals

This RFC does **not**:

1. Rewrite the OFARM Constitution.
2. Reopen assertion/history-first canonical truth.
3. Reopen governed current-state materialisation.
4. Reopen the Compliance Twin / Advisory Twin split.
5. Reopen pack merge law except for farm-intelligence-specific surface-family additions or mappings.
6. Reopen core authority law except for farm-intelligence-specific action-class additions or mappings.
7. Reopen CP11 Sustainable Autonomous Farming Charter law.
8. Reopen CP12 Cyber-Physical Mission Envelope law.
9. Reopen CP13 Learning, Experimentation, and Farm Memory law.
10. Create OFARM Social constitution or social-network law.
11. Create OFARM Exchange constitution, marketplace law, transaction law, commerce law, price discovery, settlement, logistics, or procurement law.
12. Create a public benchmark product or public leaderboard law.
13. Create production federated-learning platform implementation law.
14. Create model deployment, software deployment, adapter deployment, canary promotion, rollback, SBOM, build provenance, model-card, or generated-software governance.
15. Create CP15 agentic software delivery law.
16. Create autonomous compliance decisioning.
17. Create legal, certification, insurance, advisory, or regulatory advice.
18. Treat aggregation as anonymisation merely by assertion.
19. Treat deidentification as irreversible anonymisation merely by assertion.
20. Treat a regional alert as farm-level occurrence truth.
21. Treat a benchmark delta as compliance fact.
22. Treat received intelligence as current state.
23. Treat a federated-learning contribution as model deployment authority.
24. Treat a model-improvement signal as authority to deploy, update, fine-tune, or operate a model.
25. Treat CP13 local farm memory as shareable across farms by default.
26. Treat CP11 sustainability outputs as cross-farm claims without CP14 disclosure and claim-basis controls.
27. Treat CP12 mission, near-miss, or safety-incident signals as shareable without CP14 sovereignty and incident-disclosure controls.
28. Expand OFARM from crop-farming operational law into livestock-specific cross-farm intelligence, animal-health intelligence, welfare intelligence, herd/flock intelligence, or veterinary signal exchange law.
29. Define generic reputation, social trust, social graph, public complaint, moderation, dispute marketplace, or community-governance systems.
30. Define a universal privacy law, anonymisation standard, federated-learning protocol, model-card standard, or data-space implementation.

The full generated-software/model-deployment/adapter-deployment/SBOM/canary/rollback governance layer belongs to **CP15**.

OFARM Social, OFARM Exchange, public benchmark products, and production federated-learning platforms may be sister platforms or future profiles. They are not created by CP14.

---

## 4. Authority relationship to the Constitution

If accepted, this RFC extends the active Constitution by introducing a farm-to-farm intelligence boundary layer.

The Constitution remains higher authority. This RFC must be interpreted under existing constitutional invariants:

- canonical truth is assertion/history-first;
- current state is governed materialisation, not hidden truth;
- Advisory Twin and Compliance Twin remain logical partitions over one semantic substrate;
- events do not change current state merely by existing;
- outputs do not become truth by being generated, published, summarized, or shared;
- AI outputs, agent memory, vector-store memory, prompts, tool responses, and runtime caches are not truth stores or governance decisions;
- authority is explicit, scoped, time-bounded, traceable, and default-deny;
- sharing permission is not authority to assert, review, decide, sign, attest, operate, execute, file, or deploy;
- packs and profiles cannot mutate constitutional core meaning;
- external standards, registries, data spaces, buyer programmes, certification schemes, cooperatives, and sister platforms do not become hidden OFARM law.

CP14 adds one constitutional boundary:

```text
Intelligence that crosses farm boundaries is Advisory by default and must not create local farm truth, current state, Compliance Twin fact, claim basis, evidence sufficiency, mission authority, learning promotion, farm memory, model deployment authority, or legal/certification conclusion unless a separate governed path explicitly permits the stronger result.
```

---

## 5. Authority relationship to Platform Runtime

The Platform Runtime must realise CP14 through explicit runtime gates, not by relying on UI labels, source reputation, partner status, AI confidence, or transport success.

For farm-intelligence-sensitive paths, runtime implementations must be able to:

1. Resolve the farm-intelligence boundary context.
2. Resolve applicable `DataSovereigntyBoundary`, `SharingGrant`, `FarmIntelligenceShareGrant`, `RecipientUseConstraint`, `DerivativeUsePolicy`, `TrainingUsePolicyBinding`, revocation state, and output qualification.
3. Distinguish outgoing farm intelligence from incoming farm intelligence.
4. Preserve origin, scope, source farm or cohort class, aggregation level, redaction/deidentification posture, purpose, allowed recipients, allowed uses, prohibited uses, retention, derivative-use, training-use, and revocation posture.
5. Keep received intelligence in Advisory Twin posture by default.
6. Prevent received intelligence from mutating current state, Compliance Twin facts, local farm memory, mission authority, claim basis, or model deployment authority by itself.
7. Evaluate re-identification risk before treating aggregation or deidentification as sufficient for wider sharing.
8. Require contribution quality and poisoning/anomaly review where shared intelligence may influence multiple farms, regional alerts, benchmark outputs, or model-improvement signals.
9. Preserve correction, withdrawal, dispute, and revocation propagation traces.
10. Qualify cross-farm intelligence outputs with permitted and prohibited uses.

Transport success, API success, agent handoff success, data-space receipt, federated aggregator receipt, or recipient acknowledgement is not governance success.

---

## 6. Definitions

### FarmIntelligenceBoundary

The governed boundary controlling when farm-scoped data, evidence, summaries, learning artifacts, incident signals, alerts, benchmarks, metrics, or model-improvement signals leave, enter, or are transformed across farm boundaries.

### FarmIntelligenceSharePolicy

A policy specifying which farm-intelligence classes may be shared, with whom, for what purpose, at what aggregation/redaction/deidentification level, under what retention, derivative-use, training-use, revocation, and output constraints.

### FarmIntelligenceShareGrant

A governed grant authorising a specific farm-intelligence sharing act or class of acts. It is a specialisation of OFARM sharing law. It is not authority to assert, review, decide, attest, create local truth, create Compliance facts, dispatch missions, or deploy models.

### FarmIntelligenceContribution

A contribution of farm-scoped or farm-derived material to a cross-farm intelligence process, regional signal, benchmark, cooperative process, data-space process, federated-learning process, or model-improvement process.

### IntelligenceContributionPackage

A bounded package containing intelligence contribution payloads, source/ref lineage, redaction/deidentification/aggregation posture, permitted uses, prohibited uses, evidence basis, quality assessment, revocation posture, and output qualification requirements.

### LearningArtifactSharePackage

A governed package for sharing CP13 learning artifacts outside the originating farm context. It must not carry CP13 farm memory as local truth for a receiving farm.

### RecipientUseConstraint

A machine-readable constraint on what a recipient may do with received intelligence, including display, advisory use, benchmarking, derivative use, training use, redistribution, disclosure, retention, claim support, and deletion/withdrawal obligations.

### DerivativeUsePolicy

A policy stating whether and how received intelligence may be transformed, aggregated, summarised, used for product improvement, used in analytics, used in model development, resold, redistributed, or incorporated into downstream artifacts.

### TrainingUsePolicyBinding

A policy binding that states whether received intelligence may be used for model training, fine-tuning, retrieval corpus creation, evaluation datasets, benchmarking, or model-improvement analysis. It is not model deployment authority.

### RevocationPropagationTrace

A trace showing how revocation, withdrawal, correction, expiry, or changed permission propagates to recipients, derivatives, outputs, aggregates, training-use receipts, and downstream artifacts where required.

### RegionalAlert

A regional or cohort-level alert derived from one or more farms, external sources, models, advisors, or regional services. It may inform observation/review but is not local farm occurrence truth by itself.

### RegionalRiskSignal

A quantified or qualified regional risk indicator. It is Advisory by default and must carry scope, basis, uncertainty, evidence quality, cohort/region definition, limitations, and allowed uses.

### RegionalAlertCorrection / RegionalAlertWithdrawal

A governed correction, dispute, update, supersession, or withdrawal of a RegionalAlert or RegionalRiskSignal.

### BenchmarkDelta

A comparative measure between a farm/cohort and a benchmark reference. It is not a Compliance fact, certification conclusion, or public claim by itself.

### AggregationFloor

The minimum aggregation, cohort, k-anonymity-like, geographic, temporal, category, or other suppression threshold required before material may be treated as aggregated for a declared use.

### DeidentificationClaim / AnonymisationClaim

A claim that material has been deidentified or anonymised to a declared level. It must carry method, residual-risk, scope, and limitations. Anonymisation is not true merely because identifiers were removed.

### ReidentificationRiskAssessment

An assessment of residual re-identification risk given data fields, cohort size, geography, time, uniqueness, linkage risk, recipient context, and external auxiliary data risk.

### FederatedLearningContribution

A governed contribution to a federated or distributed learning process. It is not permission to deploy a model or alter production model behaviour.

### FederatedAggregationReceipt

A receipt from a federated or distributed aggregation process. It is evidence of aggregation participation, not proof of model safety, deployment readiness, truth, or compliance.

### ModelImprovementSignal

A signal that may inform model evaluation, analysis, or future training. It is not authority to deploy, promote, tune, or operate a model.

### TrainingUseReceipt

A record that intelligence was used, or was not used, in a training/evaluation/retrieval/model-improvement context under a declared policy binding.

### ContributionQualityAssessment

An assessment of contribution quality, including completeness, provenance, evidence, timeliness, scope fit, outliers, suspected poisoning, anomalies, and allowed use implications.

### PoisoningOrAnomalyReview

A review of suspicious, adversarial, anomalous, conflicting, or potentially poisoned intelligence contributions or regional signals.

### CrossFarmApplicabilityAssessment

An assessment of whether received intelligence is applicable to a receiving farm context, including crop, region, season, soil, variety, practice, equipment, evidence quality, uncertainty, and current-state context.

### IntelligenceOutputQualification

A required qualification envelope for cross-farm intelligence outputs, indicating Advisory/Compliance posture, source class, sharing basis, aggregation/deidentification status, evidence quality, uncertainty, applicability, allowed uses, prohibited uses, revocation/correction status, and downstream limitations.

---

## 7. Farm-to-Farm Intelligence Boundary

CP14 introduces `FarmIntelligenceBoundary` as the root concept for intelligence crossing farm boundaries.

The boundary applies whenever OFARM material is:

- shared from one farm context to another;
- received from another farm, cooperative, data space, advisor, supplier, buyer, certifier, public authority, sister platform, or AI agent;
- aggregated across farms;
- benchmarked across farms;
- converted into a regional alert or risk signal;
- packaged from CP13 learning or farm memory for cross-farm use;
- used in a federated-learning or model-improvement process;
- transformed into a deidentified, anonymised, redacted, or aggregated output;
- disclosed to a partner, buyer, certifier, data-space participant, public product, or regional intelligence service.

The boundary requires explicit resolution of:

- originating farm or cohort class;
- receiving party or recipient class;
- farm-intelligence class;
- source artifact basis;
- sharing grant or lawful/public-authority basis;
- data-sovereignty boundary;
- recipient-use constraints;
- derivative-use policy;
- training-use policy binding;
- revocation state;
- aggregation/deidentification/anonymisation posture;
- re-identification risk posture;
- quality/anomaly/poisoning review posture where applicable;
- Advisory/Compliance posture;
- output qualification.

A missing boundary resolution must not silently default to broad sharing or stronger use. Default posture is:

```text
Do not share.
If received, treat as Advisory-only and non-current-state.
If output, qualify limitations.
If uncertain, require review or refuse stronger use.
```

---

## 8. Artifact taxonomy

CP14 recognises the following farm-intelligence artifact families.

| Family | Purpose | Default twin posture |
|---|---|---|
| `FarmIntelligenceBoundary` | Boundary context for cross-farm intelligence | Governance / Advisory default |
| `FarmIntelligenceSharePolicy` | Governed policy for sharing classes and uses | Governance |
| `FarmIntelligenceShareGrant` | Specific sharing permission | Governance |
| `FarmIntelligenceContribution` | Contribution from farm or farm-derived source | Advisory/evidence candidate |
| `IntelligenceContributionPackage` | Packaged contribution with permissions and limitations | Advisory/evidence candidate |
| `LearningArtifactSharePackage` | CP13 learning artifact packaged for cross-farm use | Advisory default |
| `RegionalAlert` | Regional warning or advisory alert | Advisory |
| `RegionalRiskSignal` | Regional or cohort risk signal | Advisory |
| `RegionalAlertCorrection` | Correction/update/dispute/withdrawal | Governance / Advisory |
| `BenchmarkDelta` | Comparative benchmark result | Advisory |
| `AggregationFloor` | Minimum aggregation/suppression floor | Governance |
| `DeidentificationClaim` / `AnonymisationClaim` | Claim of deidentification/anonymisation state | Claim candidate |
| `ReidentificationRiskAssessment` | Residual privacy/commercial risk assessment | Governance/evidence |
| `DerivativeUsePolicy` | Downstream transformation/use control | Governance |
| `TrainingUsePolicyBinding` | Model-training/evaluation/retrieval-use control | Governance |
| `FederatedLearningContribution` | Distributed/federated contribution | Advisory/model-improvement candidate |
| `FederatedAggregationReceipt` | Aggregation receipt | Evidence candidate |
| `ModelImprovementSignal` | Signal for model analysis/improvement | Advisory/model-improvement candidate |
| `TrainingUseReceipt` | Training/evaluation/retrieval-use receipt | Evidence/governance |
| `RevocationPropagationTrace` | Propagation of revocation/correction/withdrawal | Governance trace |
| `RecipientUseConstraint` | Recipient allowed/prohibited use constraint | Governance |
| `IntelligenceOutputQualification` | Qualification of intelligence output | Output governance |
| `ContributionQualityAssessment` | Contribution quality/anomaly/fitness assessment | Advisory/evidence |
| `PoisoningOrAnomalyReview` | Review of suspicious or adversarial intelligence | Governance/evidence |
| `CrossFarmApplicabilityAssessment` | Applicability to receiving context | Advisory/evidence |

No family in this table creates local farm truth, Compliance fact, current state, mission dispatch authority, learning promotion, or model deployment authority merely by existing.

---

## 9. Cross-farm Advisory-default rule

Cross-farm intelligence belongs to the Advisory Twin by default.

It may:

- raise a risk flag;
- request observation;
- suggest scouting;
- support advisory comparison;
- support a local review package;
- inform a CP13 learning hypothesis;
- inform a CP11 charter-sensitive advisory evaluation;
- inform a CP12 mission preflight as advisory context;
- trigger a query, display, or output qualification;
- prepare a BridgeCandidate or other reviewed local-evaluation path.

It may not directly create:

- farm-level truth;
- accepted current state;
- Compliance Twin fact;
- accepted causal fact;
- accepted operation or mission consequence;
- CP11 sustainability claim basis;
- CP12 mission dispatch authority;
- CP13 farm memory;
- model deployment authority;
- legal/certification conclusion;
- farmer obligation;
- public benchmark claim.

A stronger use requires a separate local farm evaluation, authority, evidence, freshness, output, and promotion path under applicable OFARM law.

---

## 10. Intelligence-specific sharing law

OFARM already has general sharing and data-sovereignty law. CP14 adds intelligence-specific specialisation.

A `FarmIntelligenceShareGrant` must declare:

- grant identity;
- granting party and accountable farm-side authority;
- originating farm scope or cohort class;
- recipient party or recipient class;
- intelligence class;
- source artifact classes;
- permitted purposes;
- prohibited purposes;
- permitted output classes;
- prohibited output classes;
- retention period;
- geographic/jurisdictional restrictions where applicable;
- aggregation/redaction/deidentification requirements;
- derivative-use permission;
- training-use permission;
- redistribution/sub-sharing permission;
- revocation conditions;
- correction/withdrawal obligations;
- audit requirements.

A `FarmIntelligenceShareGrant` is not:

- authority to assert truth;
- authority to make Compliance facts;
- authority to attest or file claims;
- authority to dispatch missions;
- authority to create farm memory;
- authority to deploy models;
- authority to ignore CP11/CP12/CP13 gates;
- authority to bypass revocation.

Default posture:

```text
No grant, no sharing.
Grant does not imply derivative use.
Derivative use does not imply training use.
Training use does not imply deployment authority.
Disclosure does not imply public redistribution.
```

---

## 11. Recipient-use constraints

Every received or shared intelligence package that is not pure public reference material must carry or resolve to `RecipientUseConstraint`.

Recipient-use constraints must distinguish:

- advisory display;
- local review preparation;
- observation request;
- scouting recommendation;
- benchmark calculation;
- sustainability claim support;
- CP13 learning hypothesis support;
- CP13 farm-memory candidate support;
- CP12 mission preflight context;
- partner disclosure;
- public disclosure;
- training/evaluation/retrieval use;
- redistribution;
- commercial resale;
- derivative product creation;
- certification/legal use.

Prohibited by default unless explicitly allowed:

- public disclosure;
- redistribution;
- resale;
- training use;
- derivative product use;
- certification/legal use;
- direct Compliance Twin use;
- current-state mutation;
- mission dispatch authority;
- model deployment authority.

---

## 12. Derivative-use policy

`DerivativeUsePolicy` governs downstream transformation.

It must answer:

- may the recipient derive new metrics?
- may the recipient aggregate with other farms?
- may the recipient create benchmarks?
- may the recipient create alerts?
- may the recipient train, evaluate, or retrieve against models?
- may the recipient create commercial products?
- may the recipient redistribute derivatives?
- must the derivative carry original limitations?
- must revocation propagate to derivatives?
- must corrections propagate to derivatives?
- what residual obligations survive expiry or revocation?

Derivative use does not create deployment, compliance, attestation, or truth authority.

---

## 13. Training-use policy binding

`TrainingUsePolicyBinding` governs model-training, fine-tuning, evaluation, retrieval-corpus, benchmark-dataset, and model-improvement use.

Training-use permission must be explicit. It is separate from:

- sharing permission;
- advisory display permission;
- benchmark permission;
- derivative-use permission;
- partner disclosure permission;
- public disclosure permission;
- model deployment permission.

A `TrainingUsePolicyBinding` must declare:

- permitted model-use class;
- prohibited model-use class;
- retention and deletion posture;
- derivative-model constraints;
- attribution or lineage requirements;
- revocation propagation;
- evaluation or audit requirements;
- whether re-use in later training rounds is allowed;
- whether synthetic, augmented, or transformed data inherits restrictions.

A training-use binding is not authority to deploy, tune, promote, operate, or sell a model. CP15 governs deployment.

---

## 14. Revocation propagation

General OFARM revocation law remains in force. CP14 adds propagation requirements for cross-farm intelligence and derivatives.

`RevocationPropagationTrace` must capture:

- revocation source;
- affected grant/policy/artifact;
- affected recipients;
- affected derivative artifacts;
- affected outputs;
- affected training/evaluation/retrieval receipts;
- affected benchmark/alert artifacts where applicable;
- notification attempts;
- recipient acknowledgements;
- unresolved propagation gaps;
- limits of retroactive deletion or withdrawal;
- residual allowed use after revocation;
- audit status.

If revocation cannot practically remove all downstream derivatives, the trace must qualify that limitation. It must not assert full deletion or withdrawal unless supported.

---

## 15. Contribution package boundary

A farm intelligence contribution must not be treated as a raw truth export. It must be packaged with context and limits.

`IntelligenceContributionPackage` must carry:

- source farm or cohort posture;
- source artifact refs or source-class refs;
- contribution class;
- data minimisation posture;
- redaction/deidentification/aggregation posture;
- evidence and provenance basis;
- quality assessment;
- recipient-use constraints;
- derivative/training-use policy;
- revocation posture;
- correction/withdrawal posture;
- allowed output classes;
- prohibited output classes;
- output qualification requirements.

The package may include transformed summaries or aggregates. It must not hide whether values are measured, modelled, inferred, estimated, redacted, aggregated, deidentified, anonymised, or externally attested.

---

## 16. CP13 farm memory and local learning crossing boundary

CP13 farm memory is local/farm-scoped by default.

A `FarmMemoryEntry`, `CausalEstimate`, `LearningEvaluationTrace`, `SeasonalLearningSummary`, `LearningEvidenceBundle`, or other CP13 artifact may cross farm boundaries only through a CP14-governed package and share grant.

A `LearningArtifactSharePackage` must declare:

- originating farm scope or cohort posture;
- CP13 source artifacts;
- transformation or redaction applied;
- evidence strength and limitations;
- causal-method limitations;
- applicability limits;
- re-use constraints;
- whether receiving-farm promotion is prohibited, review-required, or allowed only through local evaluation;
- whether claim support is prohibited or requires CP11 claim-basis review;
- whether mission use is prohibited or requires CP12 preflight/local evaluation.

Receiving farms must treat shared CP13 artifacts as Advisory by default. They may not import them as local farm memory without local CP13 evaluation and promotion.

---

## 17. Cross-farm applicability assessment

`CrossFarmApplicabilityAssessment` governs whether received intelligence is relevant to a receiving farm.

It must consider, where material:

- crop;
- variety;
- crop stage;
- geography;
- season;
- climate zone;
- soil;
- management practice;
- machinery/mission context;
- CP11 charter context;
- CP12 mission/evidence context;
- CP13 learning method and evidence basis;
- sample/cohort size;
- uncertainty;
- missingness;
- bias;
- timeliness;
- receiving-farm current state;
- external standard/profile context;
- recipient-use constraints.

An applicability assessment may recommend local observation, review, or advisory consideration. It is not by itself a local truth or compliance basis.

---

## 18. Regional alerts and regional risk signals

`RegionalAlert` and `RegionalRiskSignal` may support regional intelligence while preserving local-truth boundaries.

They must carry:

- alert/signal identity;
- issuing party or service;
- source basis;
- region/cohort scope;
- temporal scope;
- target crop/context;
- evidence quality;
- uncertainty;
- aggregation/deidentification posture where source farms contributed;
- limitations;
- recommended local review or observation action;
- allowed and prohibited uses;
- correction/withdrawal posture;
- output qualification.

A regional alert may:

- warn;
- request observation;
- suggest scouting;
- trigger advisory review;
- suggest a query;
- prepare a local risk-assessment package.

A regional alert may not directly create:

- local pest/disease occurrence truth;
- local field condition;
- operation requirement;
- CP12 mission dispatch authority;
- CP11 claim basis;
- CP13 farm memory;
- Compliance Twin fact.

---

## 19. Regional alert correction, dispute, and withdrawal

Regional intelligence must be correctable and withdrawable.

`RegionalAlertCorrection` or `RegionalAlertWithdrawal` must capture:

- original alert/signal ref;
- correction, dispute, supersession, withdrawal, or false-positive class;
- reason;
- evidence basis;
- issuer/authority basis;
- affected outputs;
- affected recipients;
- revocation/propagation posture;
- display obligation;
- whether local review packages must be invalidated or re-evaluated.

A withdrawn or corrected alert must not continue to support stronger use unless a local evaluation independently justifies it.

---

## 20. Benchmark deltas and benchmark outputs

`BenchmarkDelta` is Advisory by default.

It must carry:

- benchmark class;
- cohort definition;
- aggregation floor;
- source basis;
- deidentification/anonymisation posture;
- method;
- temporal scope;
- metric profile;
- uncertainty;
- limitations;
- re-identification risk posture;
- allowed/prohibited uses;
- output qualification.

Benchmark deltas are not:

- compliance facts;
- certification conclusions;
- claim basis by themselves;
- buyer enforcement basis by default;
- public ranking authority;
- farm performance truth outside the declared method and scope.

Public or partner benchmark outputs require stronger sharing grants, aggregation floors, re-identification-risk assessment, and output qualification.

---

## 21. Aggregation floor

`AggregationFloor` declares the minimum conditions under which data may be treated as aggregated for a declared use.

It may include:

- minimum farm count;
- minimum field/parcel count;
- minimum geographic spread;
- minimum temporal spread;
- minimum category/cohort size;
- suppression thresholds;
- outlier suppression;
- dominance limits;
- uniqueness checks;
- small-cell suppression;
- recipient-class-specific restrictions;
- metric-specific restrictions.

Aggregation floors are purpose-sensitive. A floor sufficient for internal cooperative advisory use may not be sufficient for public disclosure, buyer disclosure, model training, or public benchmarking.

An aggregation floor is not an anonymisation claim by itself.

---

## 22. Deidentification and anonymisation claims

Removing direct identifiers is not enough.

A `DeidentificationClaim` or `AnonymisationClaim` must declare:

- method;
- source fields transformed or removed;
- residual fields;
- aggregation/suppression method;
- re-identification-risk assessment;
- recipient context;
- auxiliary data assumptions;
- allowed use classes;
- prohibited use classes;
- expiration/review posture;
- limitations.

`AnonymisationClaim` must be treated as stronger and harder to support than `DeidentificationClaim`.

If a claim is uncertain, contested, stale, or high-risk, public/partner disclosure must refuse, require review, or emit a qualified disposition.

---

## 23. Re-identification risk assessment

`ReidentificationRiskAssessment` must evaluate risk from:

- direct identifiers;
- quasi-identifiers;
- rare crop/region/practice combinations;
- temporal uniqueness;
- geographic uniqueness;
- small cohort size;
- outlier values;
- linkage with public datasets;
- linkage with buyer/supplier/insurer datasets;
- machinery/telemetry uniqueness;
- mission/safety incident uniqueness;
- sustainability or certification programme uniqueness;
- recipient knowledge.

Risk classes should include at least:

```text
LOW
MODERATE
HIGH
UNKNOWN_BLOCKING
```

Public disclosure, broad partner disclosure, training use, or public benchmark use must not proceed on `HIGH` or `UNKNOWN_BLOCKING` risk without explicit review and stronger controls.

---

## 24. Federated-learning contribution boundary

`FederatedLearningContribution` governs contribution into a federated or distributed learning process.

It must declare:

- contributing farm or cohort posture;
- contribution class;
- permitted training/evaluation use;
- source artifact basis;
- aggregation protocol reference where applicable;
- privacy/security posture;
- poisoning/anomaly review posture;
- revocation posture;
- derivative-model constraints;
- output qualification;
- recipient/aggregator obligations.

A `FederatedLearningContribution` is not:

- model deployment authority;
- proof of model quality;
- proof of model safety;
- authority to update production behaviour;
- authority to redistribute the contribution;
- authority to create local farm truth.

`FederatedAggregationReceipt` is a receipt of aggregation participation or result availability. It is not model deployment authority.

---

## 25. Model-improvement signals and training-use receipts

`ModelImprovementSignal` may indicate that cross-farm intelligence suggests a model, heuristic, agent, advisory workflow, ontology mapping, or analytics process might be improved.

It may support:

- review;
- evaluation;
- offline analysis;
- test creation;
- CP15 deployment candidate preparation;
- model-card evidence candidate preparation.

It may not deploy, tune, promote, operate, or silently alter model behaviour.

`TrainingUseReceipt` must record actual or prohibited use under a `TrainingUsePolicyBinding`. It must not imply lawful, authorised, or policy-compliant use unless the relevant policy and authority traces support that conclusion.

Full generated-software/model-deployment governance belongs to CP15.

---

## 26. Contribution quality assessment

`ContributionQualityAssessment` must determine whether a contribution is suitable for the declared advisory or intelligence use.

It should evaluate:

- provenance completeness;
- scope clarity;
- timestamp and freshness;
- evidence class;
- measurement/method basis;
- missingness;
- bias;
- anomalies;
- conflict with other sources;
- CP11 claim/evidence posture where sustainability-sensitive;
- CP12 verification posture where mission/incident-sensitive;
- CP13 evidence/learning quality where learning-derived;
- poisoning/adversarial risk;
- allowed use implications.

A contribution can be syntactically valid but unusable for stronger purposes.

---

## 27. Poisoning or anomaly review

Cross-farm intelligence is vulnerable to adversarial, erroneous, commercially manipulative, or low-quality signals.

`PoisoningOrAnomalyReview` must be used where a contribution, alert, benchmark, regional signal, model-improvement signal, or federated contribution is suspicious or high-impact.

Review triggers include:

- extreme outlier values;
- conflicting farm reports;
- suspicious timing;
- source identity anomalies;
- repeated coordinated submissions;
- inconsistency with local/regional evidence;
- impossible geography or crop stage;
- suspiciously beneficial commercial effect;
- failed provenance;
- failed evidence quality;
- high re-identification risk;
- suspected policy violation.

A suspicious contribution must not support regional alerts, benchmarks, training use, claim support, or model-improvement signals until review posture permits.

---

## 28. CP11 sustainability disclosure and claim interaction

CP11 remains authoritative for sustainability claim basis, charter-sensitive output qualification, evidence requirements, and sustainability disclosure posture.

CP14 adds cross-farm disclosure controls.

If cross-farm intelligence contains or supports sustainability-sensitive material, the platform must evaluate:

- CP11 `SustainabilityClaimBasis` requirements;
- CP11 output qualification;
- CP11 data-sharing/disclosure posture;
- farm-intelligence sharing grant;
- recipient-use constraints;
- aggregation/deidentification/anonymisation posture;
- re-identification risk;
- CP14 output qualification.

A sustainability benchmark or regional sustainability signal is not a sustainability claim basis by itself.

---

## 29. CP12 mission and incident intelligence interaction

CP12 remains authoritative for mission, command, telemetry, execution receipt, verification, near-miss, and physical-safety incident boundaries.

CP14 governs whether CP12-derived mission or incident information can cross farm boundaries.

Mission and incident intelligence are sensitive by default because they may reveal:

- operational practices;
- machinery capability;
- safety incidents;
- geolocation patterns;
- field layouts;
- failures, near misses, or vulnerabilities;
- contractor/vendor performance;
- insurance or liability-relevant information.

CP12 mission verification or incident records may inform regional safety learning, hazard alerts, or contribution quality review only through CP14 gates.

A shared CP12 mission/incident signal is not accepted execution truth, mission authority, safety certification, or compliance fact for another farm.

---

## 30. Current-state and materialisation boundary for received intelligence

Received farm-to-farm intelligence must not enter current-state materialisation by default.

It may:

- create an Advisory Twin signal;
- create an observation request;
- create a review request;
- create an applicability assessment;
- prepare a local evidence need;
- support a local hypothesis;
- support a local advisory scenario;
- support a BridgeCandidate or equivalent governed path.

It may not directly create:

- current crop state;
- current pest/disease occurrence;
- current field condition;
- current compliance state;
- current risk-budget use;
- local farm memory;
- accepted causal estimate.

If received intelligence is later used in current-state materialisation, it must pass the ordinary OFARM truth/evidence/review/materialisation pathway and CP14 qualification.

---

## 31. Compliance Twin boundary

Cross-farm intelligence is not Compliance Twin fact by default.

It may not directly create:

- legal nonconformity;
- certification nonconformity;
- corrective-action obligation;
- filed submission;
- attestation;
- buyer enforcement conclusion;
- public-authority conclusion;
- farm-level compliance fact.

Compliance Twin use requires separate authority, evidence, review, applicable legal/certification policy, and output-disposition gates.

---

## 32. Intelligence output qualification

`IntelligenceOutputQualification` must accompany high-consequence or outward-facing cross-farm intelligence outputs.

It must disclose or encode:

- source class;
- source scope;
- originating farm/cohort posture;
- Advisory/Compliance posture;
- evidence basis;
- quality assessment;
- applicability assessment;
- aggregation/deidentification/anonymisation posture;
- re-identification risk;
- sharing grant or authority basis;
- recipient-use constraints;
- derivative-use policy;
- training-use policy binding;
- revocation/correction status;
- uncertainty;
- limitations;
- allowed uses;
- prohibited uses;
- display requirements.

The following uses must be blocked unless a separately governed path permits them:

- current-state mutation;
- Compliance fact;
- mission dispatch authority;
- claim-bearing output;
- public disclosure;
- partner disclosure;
- training use;
- model deployment;
- farm-memory promotion;
- cross-farm redistribution.

---

## 33. Agent boundary and tool-manifest honesty

Software agents may participate in CP14 only under their existing authority envelopes and run-trace law.

Agents may:

- prepare cross-farm intelligence packages;
- evaluate share grants;
- detect missing recipient-use constraints;
- produce applicability assessments;
- request observation or review;
- prepare regional-alert candidates;
- prepare benchmark candidates;
- flag re-identification risk;
- flag poisoning/anomaly risk;
- prepare revocation propagation traces;
- summarize Advisory intelligence with qualification.

Agents may not by default:

- grant sharing permission;
- override farm data sovereignty;
- approve training use;
- approve derivative commercial use;
- approve public disclosure;
- accept Compliance Twin facts;
- create local farm memory from received intelligence;
- deploy or promote models;
- bypass CP11, CP12, CP13, or CP14 gates.

Tool manifests and capability manifests may describe CP14 support. They do not grant CP14 authority or prove CP14 conformance by themselves.

---

## 34. CP14 authority action classes

CP14 introduces farm-intelligence-specific authority action classes, subject to existing OFARM default-deny authority law.

Candidate classes:

```text
FARM_INTELLIGENCE_SHARE_GRANT_CREATE
FARM_INTELLIGENCE_SHARE_GRANT_REVOKE
FARM_INTELLIGENCE_CONTRIBUTION_CREATE
FARM_INTELLIGENCE_PACKAGE_APPROVE
RECIPIENT_USE_CONSTRAINT_SET
DERIVATIVE_USE_POLICY_APPROVE
TRAINING_USE_POLICY_APPROVE
PUBLIC_DISCLOSURE_APPROVE
PARTNER_DISCLOSURE_APPROVE
REGIONAL_ALERT_ISSUE
REGIONAL_ALERT_CORRECT
REGIONAL_ALERT_WITHDRAW
BENCHMARK_DELTA_PUBLISH
AGGREGATION_FLOOR_APPROVE
DEIDENTIFICATION_CLAIM_APPROVE
ANONYMISATION_CLAIM_APPROVE
REIDENTIFICATION_RISK_ACCEPT
FEDERATED_CONTRIBUTION_APPROVE
TRAINING_USE_RECEIPT_ACCEPT
REVOCATION_PROPAGATION_ACCEPT
POISONING_ANOMALY_REVIEW_ACCEPT
INTELLIGENCE_OUTPUT_APPROVE
```

Default posture:

- public disclosure, partner disclosure, training use, derivative commercial use, anonymisation claims, regional alert issue/withdrawal, benchmark publication, and re-identification-risk acceptance are human-governed or human-approval-required by default;
- agents may prepare candidates and traces under authority envelope, but may not approve high-consequence CP14 actions by default;
- receiving intelligence does not grant action authority.

---

## 35. Event grammar and commit-matrix implications

CP14 requires event and commit handling for farm-intelligence events.

Candidate event families:

```text
FarmIntelligenceShareGrantCreated
FarmIntelligenceShareGrantRevoked
FarmIntelligenceContributionPackaged
LearningArtifactSharePackageCreated
RecipientUseConstraintApplied
DerivativeUsePolicyApplied
TrainingUsePolicyBound
RevocationPropagationRecorded
RegionalAlertIssued
RegionalAlertCorrected
RegionalAlertWithdrawn
RegionalRiskSignalIssued
BenchmarkDeltaCreated
AggregationFloorApproved
DeidentificationClaimRecorded
AnonymisationClaimRecorded
ReidentificationRiskAssessed
FederatedLearningContributionSubmitted
FederatedAggregationReceiptRecorded
ModelImprovementSignalCreated
TrainingUseReceiptRecorded
ContributionQualityAssessed
PoisoningOrAnomalyReviewOpened
PoisoningOrAnomalyReviewClosed
IntelligenceOutputQualified
CrossFarmApplicabilityAssessed
```

Commit posture must preserve:

- grant events are governance records, not truth about underlying farm state;
- contribution events are evidence/provenance records, not truth by themselves;
- regional alerts are Advisory outputs, not local occurrence truth;
- benchmark deltas are Advisory outputs, not Compliance facts;
- model-improvement signals are Advisory/model-improvement candidates, not deployment authority;
- correction/withdrawal/revocation events must affect outputs and downstream-use posture where applicable.

---

## 36. Pack/profile surfaces

CP14 adds pack/profile surfaces for farm-intelligence policy.

Candidate surfaces:

```text
FARM_INTELLIGENCE_SHARE_POLICY
RECIPIENT_USE_CONSTRAINT_POLICY
DERIVATIVE_USE_POLICY
TRAINING_USE_POLICY
REVOCATION_PROPAGATION_POLICY
REGIONAL_ALERT_POLICY
BENCHMARK_POLICY
AGGREGATION_FLOOR_POLICY
DEIDENTIFICATION_POLICY
ANONYMISATION_CLAIM_POLICY
REIDENTIFICATION_RISK_POLICY
FEDERATED_CONTRIBUTION_POLICY
CONTRIBUTION_QUALITY_POLICY
POISONING_ANOMALY_REVIEW_POLICY
INTELLIGENCE_OUTPUT_QUALIFICATION_POLICY
```

Default merge posture should be conservative:

- sharing policy: strongest requirement or hard fail;
- recipient-use constraints: strongest requirement or hard fail;
- derivative/training-use policy: strongest requirement or hard fail;
- aggregation/deidentification/anonymisation policy: strongest requirement or hard fail;
- re-identification risk policy: strongest requirement or hard fail;
- regional alert and benchmark policy: ordered composition only where deterministic; otherwise hard fail;
- output qualification: strongest requirement.

Packs must not weaken data sovereignty, claim-basis, CP11, CP12, CP13, authority, or truth law.

---

## 37. External data-space and sister-platform boundary

CP14 may integrate with agricultural data spaces, cooperatives, public authorities, regional alert platforms, model-training platforms, OFARM Social, OFARM Exchange, or other sister platforms.

External or sister platforms may act as:

- semantic anchors;
- exchange mappings;
- evidence sources;
- grant/receipt issuers;
- aggregation services;
- regional alert issuers;
- federated-learning aggregators;
- attestation wrappers;
- sister-platform truth systems with explicit boundary.

They do not become hidden OFARM law, OFARM canonical truth, OFARM authority, CP11 claim basis, CP12 mission authority, CP13 farm memory, or CP15 deployment authority merely by integration.

Any integration must declare:

- OFARM role;
- mapping coverage;
- loss map;
- authority basis;
- data sovereignty boundary;
- output qualification;
- revocation/correction posture;
- allowed/prohibited uses.

---

## 38. Query and output gates for cross-farm intelligence

Cross-farm intelligence queries and outputs are high-consequence when they materially affect:

- sharing outside a farm;
- partner or public disclosure;
- sustainability claims;
- benchmark publication;
- regional alerting;
- CP13 farm-memory candidate use;
- CP12 mission or safety review;
- training/model-improvement use;
- legal/certification/insurance-adjacent interpretation;
- farmer obligations or perceived obligations.

Such queries/outputs must carry:

- QuerySpecification basis where applicable;
- target twin;
- scope;
- source/cohort basis;
- aggregation/deidentification posture;
- recipient-use constraints;
- revocation/correction state;
- output qualification;
- allowed/prohibited use classes;
- reconstruction trace where high-consequence.

AI summaries must not remove material limitations.

---

## 39. Farmer display, burden, and coercion controls

Cross-farm intelligence can become coercive if displayed as ranking, warning, obligation, buyer pressure, or public comparison without context.

CP14 outputs should distinguish:

- advisory signal;
- optional comparison;
- observation request;
- review-required warning;
- claim-blocking limitation;
- sharing request;
- revocation notice;
- correction/withdrawal notice;
- public/partner disclosure implication.

Farmer-facing display must not turn a regional alert, benchmark delta, peer comparison, or buyer programme signal into an apparent compliance fact or mandatory action unless a separate governed basis exists.

Request burden controls from existing OFARM policy remain in force.

---

## 40. Readiness and non-claims

Accepting CP14 would not make OFARM production-ready for farm-to-farm intelligence.

CP14 must not be used to claim:

- production federated-learning platform readiness;
- production farm-to-farm intelligence platform readiness;
- legal privacy compliance;
- anonymisation guarantee;
- public benchmark product readiness;
- OFARM Social readiness;
- OFARM Exchange readiness;
- model/software deployment readiness;
- CP15 readiness;
- autonomous cross-farm decisioning;
- certification/legal/advice readiness;
- production data-space integration readiness;
- current/default CP14 machine-contract promotion.

Allowed after accepted CP14 law, subject to conformance posture:

- model-law support for farm-intelligence boundary concepts;
- explicit Advisory-default posture for cross-farm intelligence;
- explicit distinction between sharing, authority, received intelligence, local truth, farm memory, and model deployment;
- draft/non-default machine-contract basis for CP14 testing;
- conformance fixture basis where implemented.

---

## 41. Machine-contract implications

CP14 should introduce draft/non-default machine contracts under:

```text
03_machine_contracts/drafts_non_default/farm_to_farm_intelligence/
```

Candidate schemas:

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

Schemas must be staged draft/non-default until formally promoted.

Schemas must preserve OFARM style:

- JSON Schema 2020-12;
- strict `additionalProperties: false` where possible;
- explicit refs rather than hidden runtime state;
- explicit authority/action/source/currentness/disposition enums;
- draft/non-default currentness;
- no implicit truth mutation;
- no implicit Compliance Twin promotion;
- no implicit training-use permission;
- no implicit deployment authority.

---

## 42. Conformance implications

Minimum CP14 conformance must prove:

```text
regional_alert_does_not_create_local_truth
benchmark_delta_does_not_create_compliance_fact
received_intelligence_not_current_state_by_default
farm_memory_share_without_cp14_package_fails
cross_farm_learning_artifact_import_as_farm_memory_fails
farm_intelligence_share_without_share_grant_fails
partner_disclosure_without_recipient_use_constraints_fails
training_use_without_training_policy_binding_fails
derivative_use_without_derivative_policy_fails
aggregation_claim_without_aggregation_floor_fails
anonymisation_claim_without_reidentification_assessment_fails
high_reidentification_risk_blocks_public_disclosure
regional_alert_withdrawal_blocks_downstream_alert_use
revoked_share_grant_propagates_to_outputs
federated_contribution_does_not_authorise_model_deployment
model_improvement_signal_does_not_authorise_deployment
poisoning_flag_blocks_regional_alert_publication
cp11_sustainability_benchmark_requires_claim_and_disclosure_gates
cp12_safety_incident_sharing_requires incident/disclosure gate
agent_cannot_approve_public_disclosure_by_default
valid_regional_alert_advisory_use_passes
valid_aggregated_internal_benchmark_passes
valid_federated_contribution_receipt_passes_without_deployment
valid_learning_artifact_share_package_advisory_import_passes
```

Conformance must include positive and negative fixtures. A runner that only rejects bad cases is insufficient.

---

## 43. Migration notes

Existing sharing grants and data-sovereignty records remain valid under their original scope. They do not automatically become CP14 intelligence-specific grants.

Existing CP13 farm-memory, learning, and seasonal-summary artifacts remain local/farm-scoped unless packaged through CP14.

Existing CP11 sustainability outputs remain governed by CP11; CP14 adds cross-farm disclosure and recipient-use constraints.

Existing CP12 mission/incident records remain governed by CP12; CP14 adds cross-farm sharing and incident-intelligence boundaries.

Existing regional or peer signals should be treated as Advisory and non-current-state unless reclassified under CP14.

Existing machine contracts are not promoted to current/default by CP14.

---

## 44. Risks and open questions

### 44.1 Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| CP14 becomes OFARM Social or Exchange law | High | Keep Social/Exchange explicit deferrals. |
| Received intelligence becomes local truth | Existential | Advisory-default and conformance fixtures. |
| Aggregation masquerades as anonymisation | High | Require aggregation floors and re-identification risk assessment. |
| CP13 farm memory crosses farms as truth | High | Require LearningArtifactSharePackage and local evaluation. |
| Regional alert becomes mission/operation requirement | High | Advisory-only default and output qualification. |
| Benchmark deltas become compliance facts | High | Compliance Twin boundary and use constraints. |
| Federated contribution becomes deployment authority | Existential | CP15 deferral and non-deployment rule. |
| Buyer/certifier coercion through benchmarks | High | Recipient-use constraints, display/burden controls, non-claims. |
| Poisoned signals affect many farms | High | ContributionQualityAssessment and PoisoningOrAnomalyReview. |
| Revocation fails to propagate to derivatives | High | RevocationPropagationTrace and conformance. |
| Public disclosure leaks re-identification risk | High | ReidentificationRiskAssessment and aggregation/anonymisation constraints. |

### 44.2 Open questions

- Which CP14 machine contracts should be P0 versus P1?
- Which re-identification risk model is sufficient for first conformance?
- How should public-authority regional alerts be represented without becoming hidden law?
- How should buyer/certifier programmes be bounded when they request cross-farm benchmark outputs?
- Which aggregation floors should be profile-defined rather than baseline-defined?
- How should revocation work for already-trained models? Full detail belongs to CP15.
- How should cross-border or multi-jurisdiction data-space constraints be represented?
- How should OFARM Social and OFARM Exchange sister-platform boundaries be linked without importing their law?

---

## 45. Acceptance gate

CP14 should not be accepted unless the following are true:

```text
[ ] RFC text preserves OFARM truth, current-state, twin, authority, pack, query, output, agent, CP11, CP12, and CP13 law.
[ ] RFC text clearly states cross-farm intelligence is Advisory by default.
[ ] RFC text clearly states sharing is not authority.
[ ] RFC text clearly states aggregation is not anonymisation by assertion.
[ ] RFC text clearly states regional alerts are not farm-level truth.
[ ] RFC text clearly states benchmark deltas are not compliance facts.
[ ] RFC text clearly states federated-learning contribution is not model deployment authority.
[ ] RFC text clearly states CP13 local learning may not cross farm boundaries without CP14 governance.
[ ] CP14 does not create OFARM Social, OFARM Exchange, public benchmark product law, CP15 law, or production federated-learning platform law.
[ ] Machine-contract implications are draft/non-default only.
[ ] Conformance fixtures include both positive and negative cases.
[ ] Readiness/non-claims block production farm-to-farm intelligence, legal/privacy compliance, anonymisation guarantee, model deployment, and CP15 readiness claims.
```

---

## 46. Phase 3 conclusion

This RFC draft is sufficient to proceed to CP14 Phase 4 baseline patch planning.

Phase 4 should produce controlled patch text only for:

- Constitution;
- Platform Runtime;
- Alignment Register;
- readiness memo;
- hostile-review memo.

Phase 4 should not draft schemas, create CP15 law, promote CP11/CP12/CP13 draft schemas, or merge CP14.


---

## 47. Phase 7 final reconciliation note — 2026-05-30

This final CP14 RFC candidate incorporates the Phase 6 hostile review and Phase 6.1 remediation package.

The reconciled CP14 machine-contract and conformance posture is:

```text
schema posture: draft/non-default only
schemaVersion: cp14-v0.1-draft-phase6-1-remediated
current/default promotion: none
CP15 law: not created
OFARM Social / OFARM Exchange law: not created
production farm-to-farm intelligence readiness: not claimed
production federated-learning readiness: not claimed
```

The Phase 6.1 remediation hardens this RFC's executable interpretation by requiring:

- executable CP14 conformance, not just fixture planning;
- temporally coherent, active FarmIntelligenceShareGrant records before sharing;
- disjoint allowed/prohibited/blocked use classes;
- IntelligenceOutputQualification blocks against farm truth, current state, Compliance Twin facts, mission authority, model deployment, automatic execution, and unqualified sustainability claims;
- published RegionalAlert and BenchmarkDelta outputs carry output qualification and applicability boundaries;
- AggregationFloor, DeidentificationClaim, AnonymisationClaim, and ReidentificationRiskAssessment remain distinct and traceable;
- high or unknown re-identification risk blocks public disclosure unless an explicitly governed exception exists;
- revocation propagation reaches grants, contribution packages, intelligence outputs, and training-use receipts;
- CP13 local farm-memory or learning artifacts may cross farm boundaries only through CP14-governed LearningArtifactSharePackage and CrossFarmApplicabilityAssessment paths;
- CP11 sustainability-sensitive disclosures require applicable CP11 qualification or claim-basis references;
- CP12 mission/incident disclosures require applicable CP12 qualification and redaction posture;
- federated-learning contributions and training-use receipts require training-use policy compliance and do not create CP15 deployment authority;
- poisoning/anomaly review can block downstream alert, benchmark, federated-learning, and training uses.

These hardening clauses do not expand CP14 into CP15, OFARM Social, OFARM Exchange, public benchmark product law, production federated-learning platform law, generic reputation law, legal/privacy/certification readiness, or current/default machine-contract promotion.

## 48. Final CP14 acceptance gate candidate

CP14 may proceed to final acceptance-gate review if all of the following are true:

```text
[ ] Final RFC preserves OFARM truth, current-state, twin, authority, pack, query, output, agent, CP11, CP12, and CP13 law.
[ ] Cross-farm intelligence remains Advisory by default.
[ ] Sharing does not become authority.
[ ] Received intelligence does not become local farm truth or current state.
[ ] Regional alerts do not become farm-level occurrence truth.
[ ] Benchmark deltas do not become compliance facts.
[ ] Aggregation is not treated as anonymisation.
[ ] Deidentification and anonymisation claims require risk basis and output qualification.
[ ] High re-identification risk blocks public disclosure by default.
[ ] CP13 local learning/farm memory does not cross farm boundaries without CP14 governance.
[ ] CP11 sustainability disclosure and CP12 mission/incident disclosure boundaries are preserved.
[ ] Federated-learning contribution does not create model deployment authority.
[ ] CP15 remains deferred.
[ ] OFARM Social and OFARM Exchange remain deferred.
[ ] Machine contracts remain draft/non-default.
[ ] Executable conformance runner includes positive and negative fixtures.
[ ] Readiness/non-claims block production farm-to-farm intelligence and federated-learning readiness.
```
