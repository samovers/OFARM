# OFARM Agentic Software Delivery and Model Deployment Governance RFC v0.1

Date: 2026-05-30  
Status: accepted/merged CP15 amendment; active accepted RFC authority below 00_active_baseline/ under PROJECT_AUTHORITY.md.  
Target path: `02_accepted_rfcs/OFARM_Agentic_Software_Delivery_and_Model_Deployment_Governance_RFC_v0_1.md`  
Authority tier: accepted RFC; subordinate to 00_active_baseline/ and above companion artifacts.  
Scope: introduce a bounded agentic software delivery, generated artifact, model deployment, runtime-surface release, canary/rollback, software-supply-chain, and deployment-governance contract layer without reopening OFARM truth, current-state, pack, authority, output, agent, CP11 sustainability-charter, CP12 cyber-physical mission, CP13 learning/farm-memory, or CP14 farm-to-farm intelligence law.

---

## 1. Purpose

OFARM now has a strong semantic and governance spine for the future farming platform:

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
- CP12 Cyber-Physical Mission Envelope governance for mission identity, preflight, dispatch, command integrity, geofence/no-go-zone discipline, emergency stop, human override, telemetry, execution receipt, verification, and physical-safety incident handling;
- CP13 Learning, Experimentation, and Farm Memory governance for experiments, causal estimates, learning evaluation, farm-memory promotion, seasonal learning, and learning-output qualification;
- CP14 Farm-to-Farm Intelligence Boundary governance for cross-farm sharing, regional alerts, benchmark deltas, deidentification/anonymisation claims, federated contributions, derivative use, training use, revocation propagation, poisoning/anomaly review, and intelligence-output qualification.

That foundation is necessary but not sufficient for a world in which software, adapters, mappings, prompts, workflows, models, release bundles, and deployment plans may be generated, modified, tested, and proposed by software agents.

The remaining high-consequence boundary is the delivery boundary:

```text
agent-generated code / adapter / mapping / workflow / model / prompt / policy / deployment artifact
→ passes a local build, test, scan, conformance run, canary, or tool call
→ silently becomes runtime authority, model deployment, adapter deployment, mission-control surface, cross-farm training use, sustainability-claim support, current/default schema, Compliance Twin fact, or production readiness
```

CP15 exists to make that impossible.

The core decision is:

```text
Generated software, generated adapters, generated mappings, model improvements, prompt/workflow changes, build success, test success, security scan completion, conformance run completion, capability declaration, canary success, deployment telemetry, or agent tool success do not create deployment authority, runtime authority, current/default promotion, mission authority, Compliance Twin fact, or production readiness by themselves.

Deployment requires explicit CP15 delivery envelope, authority trace, provenance/SBOM/security/conformance evidence, applicable CP11/CP12/CP13/CP14 gates, runtime-surface binding, deployment authorization, rollback posture, output qualification, and conformance evidence.
```

CP15 is governance law for agentic software delivery and model deployment. It is not a CI/CD product specification, not an MLOps platform specification, not a cloud/vendor deployment architecture, and not a production readiness claim.

---

## 2. Scope

This RFC covers agentic software delivery and model-deployment governance for OFARM runtime, model, adapter, mapping, workflow, prompt, policy, release, and deployment surfaces.

It defines:

- CP15 authority, scope, and non-goals;
- `SoftwareDeliveryBoundary`;
- generated artifact taxonomy;
- delivery lifecycle and state separation;
- agent-generated artifact provenance and agent-run linkage;
- build provenance and reproducibility evidence;
- SBOM, dependency, license, and use-constraint evidence;
- static analysis, security scan, findings, and waiver governance;
- conformance test planning and conformance run receipts;
- generated adapter and semantic-mapping governance;
- runtime-surface release binding;
- deployment candidate lifecycle;
- deployment authorisation and promotion decisions;
- deployment environment scope and blast-radius control;
- canary, telemetry, rollback, rollback readiness, and emergency disable posture;
- deployment incident and software-supply-chain incident handling;
- model deployment candidate and model-evaluation evidence;
- CP13 learning output to model deployment boundary;
- CP14 federated/model-improvement signal to deployment boundary;
- prompt, policy, and workflow deployment governance;
- capability-manifest and readiness-claim limits;
- current/default schema and contract promotion boundary;
- pack/profile/release bundle interaction;
- CP11 charter-sensitive deployment gates;
- CP12 mission/robot/command-adapter deployment gates;
- CP14 cross-farm/training-use deployment gates;
- secrets, credentials, signing keys, and deployment-authority tokens;
- artifact integrity, signing, replay resistance, and tamper evidence;
- external repository, registry, package, and model-source boundary;
- agentic rollback and emergency disable boundary;
- CP15 authority action classes;
- event grammar and commit matrix implications;
- machine-contract implications;
- conformance implications;
- migration notes;
- readiness and non-claims;
- risks and open questions.

This RFC applies to **delivery-sensitive uses**, including:

- generated code proposed for OFARM runtime use;
- generated adapters, data connectors, mapping transformations, registry bindings, or schema translators;
- generated workflows, prompts, policies, rules, or runtime scripts;
- generated model artifacts, model weights, model configurations, retrieval indexes, embedding stores, decision-support models, or inference services;
- release bundles and runtime-surface bindings;
- capability-manifest or self-description changes;
- deployment candidates and promotion decisions;
- canary releases, runtime telemetry, rollback events, emergency-disable events, and deployment incidents;
- software or model artifacts that affect CP11 charter-sensitive paths, CP12 mission/command paths, CP13 learning/farm-memory paths, or CP14 cross-farm/training-use paths;
- any output or public surface that could imply deployment readiness, production readiness, model readiness, security assurance, or conformance support.

---

## 3. Non-goals

CP15 does **not** create:

- a full CI/CD product specification;
- a prescribed cloud, edge, container, Kubernetes, registry, source-control, package-manager, or vendor deployment topology;
- a generic MLOps platform;
- automatic approval of AI-generated code;
- automatic model deployment;
- automatic prompt/workflow/policy deployment;
- automatic adapter or mapping deployment;
- automatic current/default schema or contract promotion;
- robot mission, dispatch, command, geofence, emergency-stop, or physical-safety law;
- farm-to-farm intelligence, federated-learning product, regional-alert product, public benchmark, or OFARM Social/Exchange law;
- legal, cybersecurity, safety, certification, insurance, or compliance advice;
- production software-delivery readiness;
- production model-deployment readiness;
- autonomous release readiness;
- production generated-adapter readiness;
- a guarantee that a generated artifact is safe, secure, correct, complete, or deployable.

CP15 does not weaken CP11, CP12, CP13, or CP14. A software-delivery path that touches those domains must satisfy their gates where applicable.

CP15 does not promote any CP11, CP12, CP13, CP14, or CP15 draft/non-default machine contract to current/default status. Current/default promotion remains a separate governed currentness decision.

---

## 4. Authority relationship to the Constitution

If accepted, this RFC sits below the active baseline and above companion artifacts under the active authority model.

The Constitution remains the source of model law for:

- canonical truth;
- current-state materialisation;
- pack/profile law;
- authority/delegation/sharing/revocation;
- Advisory Twin / Compliance Twin separation;
- query/output surfaces;
- AI/agent boundaries;
- conformance posture;
- no hidden truth stores;
- no hidden governance decisions.

CP15 does not create a parallel software-delivery constitution. It adds a bounded delivery-governance layer for generated artifacts, builds, scans, tests, release bundles, deployment candidates, model candidates, runtime-surface bindings, canaries, rollbacks, incidents, and deployment-output qualifications.

Where this RFC conflicts with the active baseline, the baseline wins until explicitly amended.

---

## 5. Authority relationship to Platform Runtime

The Platform Runtime remains the source of runtime law for enforcement chains, public-operation surfaces, preflight/dry-run/explain surfaces, current-state materialisation, AI/agent runtime safety, capability manifests, and deployment/runtime self-description.

CP15 adds a runtime delivery gate to the existing enforcement architecture.

For delivery-sensitive use, a conforming runtime must be able to evaluate:

- artifact identity, provenance, integrity, and signature posture;
- agent-run linkage and sponsor/controller authority;
- build provenance and reproducibility basis;
- SBOM, dependency, license, and use-constraint posture;
- static analysis, security scan, vulnerability, and waiver posture;
- conformance test plan and conformance run receipts;
- semantic-mapping loss/currentness/equivalence posture;
- runtime-surface release binding;
- deployment candidate lifecycle state;
- deployment authorisation and promotion decision;
- blast radius and environment scope;
- applicable CP11, CP12, CP13, and CP14 gates;
- canary, rollback, telemetry, incident, and emergency-disable readiness;
- readiness/output qualification and non-claim posture.

A runtime may optimise build tooling, scanning engines, container formats, registries, package managers, signing tools, deployment orchestration, telemetry ingestion, canary mechanics, and rollback mechanisms. It may not optimise by flattening CP15 delivery states, skipping authority, treating tests/scans/canary success as deployment authority, or turning generated artifacts into runtime truth by default.

---

## 6. Definitions

### SoftwareDeliveryBoundary

The governed boundary between a proposed/generated artifact and authorised OFARM runtime behaviour.

### GeneratedArtifact

A software, model, prompt, policy, mapping, adapter, workflow, test, or deployment-related artifact produced or materially modified by a software agent or automated generation process.

### GeneratedSoftwareArtifact

Generated code, library, service, runtime module, script, rule implementation, adapter implementation, validation implementation, or other executable software artifact.

### GeneratedAdapterArtifact

A generated integration, connector, parser, mapper, exporter, importer, registry-binding, API-binding, or protocol-adapter artifact.

### GeneratedWorkflowArtifact

A generated workflow, orchestration graph, job definition, pipeline, tool sequence, or scheduled runtime behaviour.

### GeneratedPromptOrPolicyArtifact

A generated or modified prompt, policy text, policy rule, evaluation rubric, system instruction, decision template, or agent behaviour-shaping artifact.

### SemanticMappingCandidate

A proposed mapping between external data/model/API semantics and OFARM concepts, including coverage, loss, uncertainty, equivalence, constraints, and currentness.

### BuildProvenance

Evidence describing build source, inputs, environment, tools, dependency set, reproducibility posture, digest, signature, and actor/run basis.

### SBOMReference

A reference to software bill-of-materials evidence, including dependencies, packages, versions, licenses, vulnerabilities, provenance, and known restrictions.

### DependencyRiskAssessment

Assessment of dependency, transitive dependency, license, origin, vulnerability, abandonment, supply-chain, or use-constraint risk.

### StaticAnalysisResult

Result of static analysis, type checking, linting, policy scanning, semantic validation, or generated-code review.

### SecurityScanResult

Result of security scanning, vulnerability detection, secret scanning, dependency scanning, container scanning, model artifact scanning, or malicious-payload review.

### SecurityFindingWaiver

Governed exception that allows a specific finding to remain unresolved under bounded scope, evidence, authority, expiry, and risk posture.

### ConformanceTestPlan

The declared set of conformance checks, fixtures, schemas, runners, gates, and expected outcomes required for a delivery candidate.

### ConformanceRunReceipt

A traceable record of conformance execution, including runner identity, input set, output results, pass/fail status, environment, timestamps, and artifacts.

### DeploymentCandidate

A software, adapter, model, prompt, workflow, policy, or release candidate proposed for deployment or runtime-surface binding.

### DeploymentPlan

The intended environment, runtime surface, scope, blast radius, sequence, canary, rollback, monitoring, and approval path for a DeploymentCandidate.

### DeploymentAuthorization

A governed authority decision allowing a specific DeploymentCandidate to be deployed under a specific DeploymentPlan, environment scope, runtime surface, blast radius, time window, and rollback posture.

### DeploymentPromotionDecision

A governed decision to promote, reject, rollback, freeze, supersede, or limit a DeploymentCandidate after review, conformance, canary, or operational evidence.

### ReleaseBundle

The set of artifacts, manifests, digests, signatures, build evidence, conformance evidence, deployment plan, rollback plan, and runtime-surface bindings that together describe a release candidate.

### RuntimeSurfaceReleaseBinding

A governed binding between a ReleaseBundle/DeploymentCandidate and a specific OFARM runtime surface, API, app surface, agent tool, mission surface, query surface, output surface, or integration surface.

### CanaryPlan

A bounded plan for limited deployment, observation, blast-radius control, stop criteria, success criteria, telemetry collection, rollback criteria, and review.

### CanaryResult

The observed result of a canary run, including telemetry, anomalies, failures, success criteria, and recommendation posture.

### RollbackPlan

A governed rollback or disable plan, including conditions, authority, target prior state, data migration reversal posture, compatibility risks, and verification.

### RollbackEvent

A record that a rollback, disable, quarantine, or fallback was executed or attempted.

### DeploymentTelemetryEnvelope

Telemetry collected from a deployment, canary, runtime surface, model, adapter, workflow, or prompt/policy change.

### RuntimeDeploymentReceipt

A runtime report that deployment was applied, acknowledged, failed, disabled, rolled back, or observed. It is evidence, not deployment authority by itself.

### ModelDeploymentCandidate

A model artifact, model configuration, inference endpoint, retrieval index, embedding store, learned policy, or model-serving change proposed for deployment.

### ModelEvaluationEvidence

Evidence assessing model behaviour, validation data, bias, uncertainty, drift, failure modes, CP13/CP14 source basis, safety posture, and allowed/prohibited use.

### PromptPolicyChangeCandidate

A prompt, policy, rubric, instruction, guardrail, agent configuration, workflow rule, or tool-use policy proposed for runtime effect.

### WorkflowDeploymentCandidate

A generated or modified workflow, orchestration graph, agent sequence, tool chain, scheduled process, or event-driven runtime behaviour proposed for deployment.

### SoftwareSupplyChainIncident

A suspected or confirmed incident affecting software, model, dependency, build, registry, signing, deployment, package, or release-chain integrity.

### DeploymentIncident

A suspected or confirmed runtime incident caused by or materially involving a deployment, release, model, adapter, workflow, prompt/policy change, or rollback failure.

### DeploymentOutputQualification

The required result qualification for outputs or surfaces that describe software/model readiness, deployment status, release status, conformance status, security status, canary result, or production readiness.

---

## 7. SoftwareDeliveryBoundary

CP15 introduces `SoftwareDeliveryBoundary` as the governed boundary separating proposal from runtime effect.

A generated or modified artifact may pass through states such as:

```text
GENERATED
SUBMITTED
BUILT
SCANNED
TESTED
CONFORMANCE_TESTED
REVIEWED
CANDIDATE
AUTHORISED_FOR_CANARY
CANARY_RUNNING
CANARY_PASSED
CANARY_FAILED
AUTHORISED_FOR_DEPLOYMENT
DEPLOYED
ROLLED_BACK
DISABLED
QUARANTINED
SUPERSEDED
REJECTED
```

No state before explicit deployment authorisation creates runtime authority.

A generated artifact is not deployed merely because it exists, compiles, tests pass, static analysis passes, a security scan passes, a conformance run passes, a canary passes, an agent recommends it, or a manifest declares the capability.

---

## 8. Generated artifact taxonomy

CP15 recognises generated or agent-modified artifact families:

- `GeneratedSoftwareArtifact`;
- `GeneratedPatchArtifact`;
- `GeneratedAdapterArtifact`;
- `GeneratedWorkflowArtifact`;
- `GeneratedPromptOrPolicyArtifact`;
- `SemanticMappingCandidate`;
- `ConformanceTestArtifact`;
- `ModelDeploymentCandidate`;
- `PromptPolicyChangeCandidate`;
- `WorkflowDeploymentCandidate`;
- `ReleaseBundle`;
- `DeploymentCandidate`.

Every generated artifact that may affect OFARM runtime behaviour must declare:

- artifact identity;
- artifact family;
- source basis;
- generator identity;
- agent run trace where generated by software agent;
- sponsor/controller basis;
- intended runtime surface;
- affected domains and gates;
- integrity/digest/signature posture;
- authority status;
- conformance status;
- deployment status;
- allowed/prohibited use posture;
- rollback/disable posture where applicable.

There is no generic `AgentGeneratedThing` truth bucket. A generated artifact must resolve to a declared artifact family and governed lifecycle.

---

## 9. Delivery lifecycle and state separation

CP15 separates:

```text
generation
submission
build
analysis
scan
conformance testing
review
deployment candidacy
authorisation
canary
deployment
runtime observation
promotion
rollback / disable
incident / quarantine
supersession
```

The following shortcuts are prohibited:

```text
build success → deployment authority
test success → deployment authority
scan success → deployment authority
conformance pass → deployment authority
canary pass → production promotion
agent approval phrase → authority
manifest declaration → current/default support
deployment receipt → production readiness
telemetry healthy → automatic promotion
model evaluation success → model deployment authority
CP13 learning output → model deployment
CP14 model-improvement signal → model deployment
```

---

## 10. Agent-generated artifact provenance and run linkage

A generated artifact produced by a software agent must carry or link:

- `AgentActorshipBinding`;
- `AgentAuthorityEnvelope`;
- `AgentRunEnvelope`;
- `AgentRunTrace`;
- tool invocation traces where relevant;
- sponsor/controller identity;
- prompt/config/model/tool basis where material;
- authority limits;
- blocked-action traces where an agent attempted a prohibited deployment, signing, promotion, or current/default action.

Agent-generated status is provenance. It is not approval, authority, safety, evidence sufficiency, conformance, or deployment right.

A human, governance process, or explicitly bounded policy authority remains required for high-consequence deployment authorisation by default.

---

## 11. Build provenance and reproducibility evidence

A delivery candidate that includes executable software must declare build provenance.

`BuildProvenance` should include:

- source artifact refs;
- repository/source refs;
- commit/digest refs;
- generator/actor refs;
- build environment identity;
- toolchain identity;
- dependency lock/basis;
- reproducibility posture;
- artifact digest;
- build logs/results;
- signature posture;
- produced artifacts;
- timestamps;
- known limitations.

Build success is evidence. It is not deployment authority.

A non-reproducible build may still be considered in low-risk contexts if explicitly qualified and reviewed. It must not silently support high-consequence runtime surfaces, mission surfaces, Compliance Twin effects, or production-readiness claims.

---

## 12. SBOM, dependency, license, and use-constraint evidence

A deployment candidate must declare SBOM/dependency posture appropriate to its risk class.

Required posture may include:

- SBOM reference;
- dependency list;
- transitive dependency posture;
- known vulnerabilities;
- license constraints;
- provenance constraints;
- maintenance/abandonment risks;
- package-source trust;
- registry trust;
- model-source trust;
- export/use restrictions;
- forbidden dependency classes;
- waiver basis where findings are not resolved.

A dependency or license scan is not enough by itself. Findings, use constraints, waivers, and risk decisions must be governed.

---

## 13. Static analysis, security scan, findings, and waiver governance

A deployment candidate must have analysis and scanning appropriate to its intended surface and blast radius.

`StaticAnalysisResult` and `SecurityScanResult` may include:

- scan type;
- scanner/tool identity;
- input artifacts;
- findings;
- severity;
- exploitability or impact class;
- false-positive determinations;
- waiver refs;
- unresolved finding posture;
- affected runtime surfaces;
- deployment blocking status.

A high-severity unresolved finding is deployment-blocking by default for high-consequence runtime surfaces.

A waiver must be scoped, approved, evidence-linked, expiry-aware, and traceable. Waiver existence is not a general clearance.

---

## 14. Conformance test plan and conformance run receipt

CP15 requires delivery candidates to declare conformance posture.

A `ConformanceTestPlan` identifies:

- required schema validations;
- required conformance runners;
- required fixture sets;
- required positive/negative tests;
- required cross-record tests;
- required semantic-hardening checks;
- affected OFARM domains;
- acceptance thresholds;
- non-applicable checks and basis.

A `ConformanceRunReceipt` records:

- test plan ref;
- runner identity;
- input fixture set;
- executed checks;
- pass/fail results;
- skipped checks and basis;
- execution environment;
- timestamps;
- output artifacts;
- limitations.

A conformance pass is evidence. It is not deployment authorisation by itself.

---

## 15. Generated adapter and semantic mapping governance

Generated adapters and mappings are high-risk because they can mutate meaning at integration boundaries.

A generated adapter or mapping candidate must declare:

- source system/API/schema/protocol;
- target OFARM concepts;
- mapping coverage;
- loss map;
- field/unit transformations;
- identity binding posture;
- time/currentness handling;
- evidence/provenance handling;
- authority and sharing handling;
- affected twin(s);
- affected current-state/materialisation path;
- affected CP11/CP12/CP13/CP14 gates;
- conformance evidence.

A generated adapter must not:

- convert external payloads into canonical truth by default;
- make registry/API success into evidence sufficiency;
- bypass authority;
- bypass current-state freshness;
- bypass CP11 sustainability gate;
- bypass CP12 mission gate;
- bypass CP13 learning/farm-memory gate;
- bypass CP14 data-sharing boundary;
- silently promote external standards, buyer programmes, vendor semantics, or model outputs into OFARM core meaning.

---

## 16. Runtime surface release binding

Deployment must bind to declared runtime surfaces.

Examples:

- public operation surface;
- application-builder operation;
- query surface;
- output/DocumentAssembly/PassportView surface;
- agent tool surface;
- Advisory Twin world-model surface;
- CP11 charter gate surface;
- CP12 mission/preflight/command surface;
- CP13 learning/farm-memory surface;
- CP14 farm-to-farm intelligence surface;
- import/export adapter surface;
- conformance runner surface;
- administrative/governance surface.

`RuntimeSurfaceReleaseBinding` must specify:

- target surface;
- intended change;
- allowed use;
- prohibited use;
- authority required;
- conformance required;
- rollback path;
- monitoring requirements;
- output qualification;
- affected data/twin/current-state surfaces.

A release bundle not bound to a runtime surface is not deployable.

---

## 17. Deployment candidate lifecycle

A `DeploymentCandidate` may progress through governed states, including:

```text
PROPOSED
BUILT
SCANNED
CONFORMANCE_TESTED
REVIEW_REQUIRED
REJECTED
APPROVED_FOR_CANARY
CANARY_RUNNING
CANARY_FAILED
CANARY_PASSED
APPROVED_FOR_DEPLOYMENT
DEPLOYED
DISABLED
ROLLED_BACK
SUPERSEDED
QUARANTINED
```

State progression must be traceable. High-consequence states must require authority traces and supporting evidence.

A candidate may not jump from `PROPOSED`, `BUILT`, `SCANNED`, or `CONFORMANCE_TESTED` directly into `DEPLOYED` without deployment authorisation.

---

## 18. Deployment authorisation and promotion decision

`DeploymentAuthorization` is the governed authority decision allowing a deployment under a particular plan, environment, runtime surface, blast radius, and time window.

It must not be inferred from:

- agent output;
- build success;
- test success;
- scan success;
- conformance success;
- canary success;
- capability manifest declaration;
- human-readable approval note without authority trace;
- external registry acceptance;
- vendor deployment acknowledgement.

`DeploymentPromotionDecision` governs whether a candidate is promoted, rejected, rolled back, quarantined, superseded, or limited after review.

High-consequence deployment authorisation and promotion are human-governed or explicitly bounded policy-governed by default.

---

## 19. Deployment environment scope and blast-radius control

A `DeploymentPlan` must declare environment and blast-radius scope.

Examples:

```text
LOCAL_DEV
SIMULATION_ONLY
SANDBOX
TEST_FARM
SINGLE_FARM_ADVISORY
SINGLE_FARM_OPERATIONAL
MULTI_FARM_ADVISORY
REGIONAL_ADVISORY
MISSION_CRITICAL
COMPLIANCE_AFFECTING
PUBLIC_OUTPUT_AFFECTING
```

Blast-radius expansion requires governance.

A candidate approved for simulation, sandbox, or advisory use may not silently deploy to mission-critical, compliance-affecting, public-output, or multi-farm surfaces.

---

## 20. Canary, telemetry, rollback, and rollback-readiness posture

High-consequence deployment should have canary and rollback posture where practical.

`CanaryPlan` must define:

- scope;
- duration;
- success criteria;
- stop criteria;
- monitoring;
- affected users/farms/surfaces;
- rollback/disable path;
- escalation and review.

`CanaryResult` is evidence. It is not production promotion by itself.

`RollbackPlan` must define:

- rollback target;
- conditions;
- authority;
- compatibility risks;
- data migration posture;
- verification;
- fallback state;
- limitations.

A deployment without rollback posture must be qualified and may be blocked for high-consequence surfaces.

---

## 21. Deployment incident and software-supply-chain incident handling

CP15 introduces incident handling for delivery and runtime software/model surfaces.

A `SoftwareSupplyChainIncident` may involve:

- compromised dependency;
- malicious generated code;
- registry poisoning;
- credential/key compromise;
- signature mismatch;
- tampered artifact;
- model artifact compromise;
- dependency substitution;
- license/use-constraint violation;
- conformance runner compromise.

A `DeploymentIncident` may involve:

- runtime failure;
- unsafe recommendation path;
- mission-surface impact;
- output-qualification failure;
- data leakage;
- cross-farm disclosure failure;
- model drift;
- rollback failure;
- canary failure;
- security finding exploitation.

Incidents do not automatically create compliance facts, but they must be recorded, qualified, reviewed, and routed according to severity and affected surfaces.

---

## 22. Model deployment candidate and model-evaluation evidence

A `ModelDeploymentCandidate` is not a deployed model merely because it was trained, evaluated, benchmarked, fine-tuned, generated, or recommended.

Model deployment requires:

- model artifact identity;
- source/training basis;
- evaluation evidence;
- allowed/prohibited use;
- affected surfaces;
- CP13 learning boundary checks;
- CP14 training-use/federated contribution checks where applicable;
- drift/monitoring posture;
- rollback/disable posture;
- output qualification;
- authority trace.

`ModelEvaluationEvidence` must declare:

- evaluation dataset/source basis;
- scope and applicability;
- bias/missingness/uncertainty;
- out-of-domain limits;
- failure modes;
- safety/posture limits;
- CP11/CP12/CP13/CP14 dependencies;
- model-card or external artifact references where used;
- limitations and prohibited use.

A model-improvement signal from CP14 or a learning output from CP13 is not model deployment authority.

---

## 23. CP13 learning output to model deployment boundary

CP13 local learning, causal estimates, farm memory, seasonal summaries, and learning-promotion decisions may inform model-development or model-evaluation work.

They do not:

- authorise model deployment;
- authorise runtime-surface changes;
- create model readiness;
- create current/default promotion;
- create Compliance Twin fact;
- create public claim support;
- create cross-farm training use.

A model deployment path using CP13 artifacts must declare:

- learning artifact refs;
- learning-output qualification;
- farm-memory retrieval qualification;
- learning-promotion status;
- evidence sufficiency;
- bias/missingness/uncertainty;
- allowed/prohibited use;
- authority and consent posture.

---

## 24. CP14 federated/model-improvement signal to deployment boundary

CP14 federated contributions, aggregation receipts, model-improvement signals, training-use receipts, benchmark deltas, regional alerts, and intelligence outputs may inform model development.

They do not:

- create deployment authority;
- create production model readiness;
- create training-use authority beyond their declared scope;
- erase revocation obligations;
- remove deidentification/anonymisation limitations;
- authorise public claims;
- create current/default promotion.

A deployment path using CP14 artifacts must respect:

- share grants;
- recipient-use constraints;
- derivative-use policy;
- training-use policy binding;
- reidentification-risk posture;
- revocation propagation;
- poisoning/anomaly review;
- intelligence-output qualification.

---

## 25. Prompt, policy, and workflow deployment governance

Prompt, policy, and workflow changes can materially change agent behaviour without changing compiled code.

A `PromptPolicyChangeCandidate` or `WorkflowDeploymentCandidate` must declare:

- target agent/tool/workflow/runtime surface;
- affected authority/action classes;
- affected output dispositions;
- affected CP11/CP12/CP13/CP14 gates;
- test/conformance posture;
- review and approval posture;
- rollback/disable path;
- allowed/prohibited use;
- monitoring/incident posture.

A prompt or workflow update is not low-risk merely because it is “configuration”. If it changes agent behaviour, output qualification, mission preparation, data sharing, claim generation, or learning promotion, it is deployment-sensitive.

---

## 26. Capability manifest and readiness-claim limits

Capability manifests and tool manifests remain descriptive, not dispositive.

A manifest may describe:

- supported CP15 artifact families;
- available validators/scanners/builders/runners;
- supported deployment surfaces;
- supported conformance suites;
- supported rollback/canary features;
- known limitations.

A manifest may not create:

- authority;
- approval;
- evidence sufficiency;
- conformance success;
- deployment authorisation;
- production readiness;
- current/default support;
- security certification;
- model deployment readiness.

Readiness claims must be supported by CP15 qualification and evidence. “Tool supports deployment” does not mean “deployment is authorised.”

---

## 27. Current/default schema and contract promotion boundary

Current/default schema and contract promotion remains a governed currentness act.

CP15 must explicitly protect this boundary:

```text
Generated schema / generated contract / generated currentness file / passing schema validation / passing conformance runner / agent recommendation / release bundle inclusion
→ does not become current/default by itself.
```

Promotion to current/default requires:

- explicit currentness-promotion decision;
- authority trace;
- active artifact set update;
- package/steward validation;
- conformance evidence;
- readiness/non-claim review;
- supersession/invalidation handling;
- public/output qualification where applicable.

---

## 28. Pack/profile/release bundle interaction

A release bundle may include packs, profile changes, adapters, mappings, schemas, policy updates, prompts, workflows, and runtime code.

CP15 does not change pack law. It adds delivery governance for release bundles that include or affect packs/profiles.

A release bundle must declare:

- pack/profile changes;
- touched surfaces;
- merge results;
- affected CP11/CP12/CP13/CP14 surfaces;
- compatibility/conflict posture;
- conformance evidence;
- activation authority;
- rollback/supersession posture.

Pack activation is not deployment authorisation unless explicitly linked through an accepted authority path.

Deployment authorisation is not pack activation unless explicitly linked through an accepted authority path.

---

## 29. CP11 charter-sensitive deployment gates

A deployment path is CP11-sensitive when it affects:

- sustainability constraints/objectives/trade-offs;
- sustainability evidence or claim basis;
- charter evaluation traces;
- sustainability output qualification;
- charter exception/breach handling;
- risk/regret budget behaviour;
- sustainability-sensitive agent/workflow behaviour;
- sustainability pack/profile surfaces.

Such deployment must resolve applicable CP11 gates. A software release must not weaken CP11 evidence, claim, output, exception, breach, or objective/constraint law by generated code or configuration.

---

## 30. CP12 mission/robot/command-adapter deployment gates

A deployment path is CP12-sensitive when it affects:

- mission preparation;
- preflight;
- dispatch authorisation;
- command envelope/integrity;
- geofence/no-go-zone handling;
- emergency stop/human override/local fallback;
- telemetry/receipt/verification handling;
- mission output qualification;
- mission incident processing;
- robot/machine/adapter surfaces.

Such deployment must resolve applicable CP12 gates. A generated adapter, workflow, model, or prompt may not become mission authority, command authority, or execution truth by deployment alone.

---

## 31. CP13 learning/farm-memory deployment gates

A deployment path is CP13-sensitive when it affects:

- experiment protocols;
- trial designs;
- outcome measures;
- learning evidence;
- causal estimates;
- learning promotion;
- farm-memory entry, retrieval, invalidation, or seasonal summary;
- learning output qualification;
- model training/evaluation derived from CP13 artifacts.

Such deployment must resolve applicable CP13 gates. A deployment must not convert farm memory into hidden current state, agent memory into farm memory, or causal estimates into compliance facts.

---

## 32. CP14 cross-farm/training-use deployment gates

A deployment path is CP14-sensitive when it affects:

- cross-farm contribution packages;
- regional alerts;
- benchmark deltas;
- deidentification/anonymisation claims;
- reidentification risk;
- federated contribution/aggregation;
- model-improvement signals;
- training-use receipts;
- recipient-use constraints;
- revocation propagation;
- intelligence-output qualification.

Such deployment must resolve applicable CP14 gates. A deployment must not convert federated contribution or model-improvement signal into model deployment authority.

---

## 33. Secrets, credentials, signing keys, and deployment authority tokens

CP15 must treat credentials, secrets, signing keys, deployment tokens, registry tokens, runtime service credentials, and model registry credentials as high-consequence delivery materials.

A generated artifact, agent, workflow, or tool may not obtain or use deployment authority tokens merely because it can call a tool or write a manifest.

Secrets/credentials/key posture must include:

- scope;
- holder/controller;
- use class;
- rotation/expiry;
- revocation;
- audit trace;
- storage/access posture;
- incident response;
- separation from model/prompt memory;
- non-disclosure into outputs or training artifacts.

---

## 34. Artifact integrity, signing, replay resistance, and tamper evidence

High-consequence delivery artifacts should have integrity posture.

This may include:

- content digest;
- signed manifest;
- source digest;
- build digest;
- SBOM digest;
- release bundle digest;
- deployment authorization digest;
- command/deployment replay nonce;
- expiry;
- recipient/environment binding;
- tamper evidence;
- verification result.

Signature or digest presence is evidence. It is not by itself correctness, security, authority, or deployment readiness.

---

## 35. External repository, registry, package, and model-source boundary

External repositories, package registries, model registries, artifact stores, vendor APIs, code-generation systems, and model providers are external sources.

They may provide:

- source references;
- package artifacts;
- model artifacts;
- signatures;
- SBOMs;
- advisories;
- vulnerabilities;
- license data;
- attestations;
- provenance evidence.

They do not become hidden OFARM law, authority, truth, evidence sufficiency, deployment readiness, or current/default promotion by default.

External source use must be declared and evaluated under CP15 delivery governance.

---

## 36. Agentic rollback and emergency disable boundary

Agents may recommend rollback, prepare rollback plans, execute allowed low-risk disable actions where explicitly authorised, and raise emergency-disable alerts.

Agents may not by default:

- rollback production/high-consequence surfaces;
- disable mission-critical surfaces;
- change current/default contracts;
- revoke external sharing/training policy;
- erase evidence;
- delete incident traces;
- hide failed deployments.

Emergency disable and rollback authority must be explicit, scoped, traceable, and reviewable.

Rollback/disable events are evidence of operational action, not proof that the prior problem is resolved or that a new version is safe.

---

## 37. Event grammar and commit matrix implications

CP15 requires event grammar support for software delivery and model deployment events.

Candidate events include:

- `GeneratedArtifactSubmitted`;
- `BuildProvenanceRecorded`;
- `SBOMRecorded`;
- `DependencyRiskAssessed`;
- `StaticAnalysisCompleted`;
- `SecurityScanCompleted`;
- `SecurityFindingWaiverRequested`;
- `SecurityFindingWaiverApproved`;
- `ConformanceTestPlanDeclared`;
- `ConformanceRunCompleted`;
- `DeploymentCandidateSubmitted`;
- `DeploymentAuthorizationRequested`;
- `DeploymentAuthorizationApproved`;
- `DeploymentAuthorizationDenied`;
- `CanaryStarted`;
- `CanaryCompleted`;
- `DeploymentApplied`;
- `RuntimeDeploymentReceiptRecorded`;
- `DeploymentPromotionApproved`;
- `RollbackPlanApproved`;
- `RollbackExecuted`;
- `DeploymentIncidentRecorded`;
- `SoftwareSupplyChainIncidentRecorded`;
- `EmergencyDisableExecuted`;
- `CurrentDefaultPromotionRequested`;
- `CurrentDefaultPromotionApproved`;
- `CurrentDefaultPromotionDenied`.

These events do not automatically create deployment truth, production readiness, current/default promotion, or Compliance Twin fact. Their consequences depend on accepted event consequence, authority, evidence, review, promotion, and currentness law.

---

## 38. CP15 authority action classes

CP15 likely requires authority action classes such as:

```text
DELIVERY_SUBMIT_GENERATED_ARTIFACT
DELIVERY_RECORD_BUILD_PROVENANCE
DELIVERY_RECORD_SBOM
DELIVERY_RECORD_SECURITY_SCAN
DELIVERY_APPROVE_SECURITY_WAIVER
DELIVERY_DECLARE_CONFORMANCE_PLAN
DELIVERY_RECORD_CONFORMANCE_RUN
DELIVERY_SUBMIT_DEPLOYMENT_CANDIDATE
DELIVERY_APPROVE_CANARY
DELIVERY_APPROVE_DEPLOYMENT
DELIVERY_APPROVE_PROMOTION
DELIVERY_APPROVE_ROLLBACK
DELIVERY_EXECUTE_ROLLBACK
DELIVERY_EXECUTE_EMERGENCY_DISABLE
DELIVERY_BIND_RUNTIME_SURFACE
DELIVERY_PROMOTE_CURRENT_DEFAULT_CONTRACT
DELIVERY_PROMOTE_MODEL_DEPLOYMENT
DELIVERY_APPROVE_PROMPT_POLICY_CHANGE
DELIVERY_APPROVE_WORKFLOW_DEPLOYMENT
DELIVERY_RECORD_DEPLOYMENT_INCIDENT
DELIVERY_RESOLVE_DEPLOYMENT_INCIDENT
DELIVERY_RECORD_SUPPLY_CHAIN_INCIDENT
DELIVERY_RESOLVE_SUPPLY_CHAIN_INCIDENT
```

Default posture:

- software agents may prepare candidates, evidence, plans, test runs, scans, and review packages within their authority envelope;
- software agents may not approve high-consequence deployment, model deployment, current/default promotion, or emergency disable by default;
- current/default promotion is human-governed or explicitly bounded policy-governed by default;
- mission-sensitive deployment requires CP12-aware approval;
- cross-farm/training-sensitive deployment requires CP14-aware approval;
- claim/output-sensitive deployment requires CP11-aware approval.

---

## 39. Interaction with Advisory Twin

Most generated artifacts, model candidates, workflow candidates, prompt/policy candidates, semantic-mapping candidates, canary analyses, and model-evaluation results belong to Advisory Twin posture by default.

They may:

- propose changes;
- prepare evidence;
- run tests/scans/conformance;
- produce candidate mappings;
- recommend deployment;
- recommend rollback;
- recommend disable;
- prepare review packages.

They may not directly create:

- runtime deployment;
- Compliance Twin fact;
- current/default status;
- mission authority;
- farm truth;
- sustainability claim readiness;
- cross-farm data-use authority;
- production readiness.

---

## 40. Interaction with Compliance Twin

CP15 artifacts may become relevant to Compliance Twin surfaces only through explicit review and promotion paths.

Examples:

- evidence that a conformance run was performed;
- evidence that a deployment was authorised;
- evidence that a rollback occurred;
- evidence that a vulnerability was waived;
- evidence that a current/default promotion was approved;
- evidence that a deployment incident occurred.

These are not themselves Compliance Twin facts unless accepted through the relevant OFARM review/promotion path.

---

## 41. Interaction with current-state materialisation

Deployment status, release status, contract currentness, active runtime-surface binding, active model deployment, active prompt/policy configuration, and active conformance status may be materialised as current state only when derived from accepted in-force records.

A deployment receipt, telemetry record, external registry status, agent memory, local file presence, or generated manifest does not create current deployment state by itself.

High-consequence outputs relying on current deployment state must satisfy current-state freshness and reconstruction requirements.

---

## 42. Interaction with packs

CP15 may introduce pack/profile surfaces for:

- delivery policy;
- required scanners;
- required conformance suites;
- security finding thresholds;
- waiver rules;
- deployment environment classes;
- canary/rollback policy;
- runtime-surface binding policy;
- model deployment policy;
- prompt/policy/workflow deployment policy;
- current/default promotion policy;
- CP11/CP12/CP13/CP14 gate requirements.

Pack/profile changes must not weaken baseline CP15 invariants unless explicitly governed. Conflicting delivery policy surfaces should hard-fail or require review under existing pack merge law.

---

## 43. Interaction with agents and capability manifests

CP15 strengthens existing agent and capability-manifest law.

An agent/tool/capability may declare:

- generation capability;
- build capability;
- scanning capability;
- conformance runner capability;
- deployment-plan preparation capability;
- canary/telemetry summarisation capability;
- rollback recommendation capability.

Such declarations are not authority.

The manifest must not claim CP15 deployment readiness unless it can describe:

- supported artifact families;
- supported evidence types;
- supported gates;
- supported conformance suites;
- supported rollback/disable posture;
- limitations;
- non-current/default posture where applicable.

Tool success remains separate from governance success.

---

## 44. Machine-contract implications

CP15 likely requires draft/non-default machine contracts for:

- `SoftwareDeliveryBoundary`;
- `GeneratedSoftwareArtifact`;
- `GeneratedPatchArtifact`;
- `GeneratedAdapterArtifact`;
- `GeneratedWorkflowArtifact`;
- `GeneratedPromptOrPolicyArtifact`;
- `SemanticMappingCandidate`;
- `AdapterGenerationRequest`;
- `BuildProvenance`;
- `SBOMReference`;
- `DependencyRiskAssessment`;
- `StaticAnalysisResult`;
- `SecurityScanResult`;
- `SecurityFindingWaiver`;
- `ConformanceTestPlan`;
- `ConformanceRunReceipt`;
- `DeploymentCandidate`;
- `DeploymentPlan`;
- `DeploymentAuthorization`;
- `DeploymentPromotionDecision`;
- `ReleaseBundle`;
- `RuntimeSurfaceReleaseBinding`;
- `CanaryPlan`;
- `CanaryResult`;
- `RollbackPlan`;
- `RollbackEvent`;
- `DeploymentTelemetryEnvelope`;
- `RuntimeDeploymentReceipt`;
- `ModelDeploymentCandidate`;
- `ModelEvaluationEvidence`;
- `PromptPolicyChangeCandidate`;
- `WorkflowDeploymentCandidate`;
- `SoftwareSupplyChainIncident`;
- `DeploymentIncident`;
- `DeploymentOutputQualification`;
- `DeploymentEnvironmentScope`;
- `ArtifactIntegrityBasis`;
- `SigningKeyUseTrace`;
- `SecretUseTrace`;
- `CurrentDefaultPromotionDecision`.

These contracts should be staged under draft/non-default paths until currentness promotion is explicitly approved.

---

## 45. Conformance implications

CP15 requires executable conformance, not prose-only governance.

Minimum conformance fixture families should include:

- generated artifact cannot deploy without deployment authorisation;
- build success does not create deployment authority;
- conformance run success does not create deployment authority;
- canary success does not create production promotion;
- deployment candidate cannot skip build/security/conformance evidence where required;
- high-severity unresolved security finding blocks high-consequence deployment;
- security waiver requires authority, scope, evidence, and expiry;
- generated adapter with mapping loss cannot be deployed to high-consequence surface without review/qualification;
- CP11-sensitive deployment requires charter gate traces;
- CP12-sensitive mission adapter deployment requires mission-surface safety gates;
- CP13 learning output cannot become model deployment authority;
- CP14 model-improvement signal cannot become model deployment authority;
- prompt/policy change cannot change agent authority without approval;
- runtime-surface binding cannot target undeclared surface;
- deployment outside authorised environment scope fails;
- current/default schema promotion requires currentness promotion decision;
- rollback plan required for high-consequence deployment;
- deployment receipt does not create production readiness;
- output qualification blocks production-readiness claims without evidence;
- external registry acceptance does not create OFARM deployment authority;
- revoked signing key blocks release bundle;
- signing/integrity mismatch blocks deployment;
- deployment incident blocks or qualifies further promotion.

---

## 46. Migration notes

Existing generated artifacts, scripts, adapters, prompts, workflows, models, release bundles, or deployment notes should not be retroactively treated as CP15-authorised deployments.

On CP15 acceptance:

- existing generated/delivery artifacts may be inventoried;
- deployment-sensitive artifacts should be classified by family and surface;
- current/default status must remain governed by existing currentness records;
- CP11/CP12/CP13/CP14 draft/non-default machine contracts remain draft/non-default;
- existing conformance runners remain current only where currentness maps say so;
- existing release/support notes should be qualified if they imply readiness without CP15 evidence.

CP15 does not require immediate implementation of a production deployment platform. It establishes the governance law and draft contract surface for future implementation.

---

## 47. Readiness and non-claims

CP15 does not claim:

- production software-delivery readiness;
- production model-deployment readiness;
- generated-adapter deployment readiness;
- generated-workflow deployment readiness;
- autonomous release readiness;
- cybersecurity certification;
- legal/security/compliance advice;
- cloud/vendor deployment readiness;
- generic MLOps readiness;
- current/default promotion of CP11, CP12, CP13, CP14, or CP15 schemas;
- CP12 robot/mission production readiness;
- CP14 federated-learning platform readiness;
- public benchmark product readiness.

After acceptance, CP15 may claim only bounded model-law support for agentic software-delivery and model-deployment governance, subject to conformance and steward validation.

---

## 48. Risks and open questions

Open risks:

- how to distinguish low-risk configuration changes from high-consequence prompt/policy/workflow deployment;
- how to define minimum security scan depth without becoming a security standard;
- how to handle external package/model registries without vendor lock-in;
- how to model generated semantic mappings without excessive schema complexity;
- how to define current/default promotion contracts without destabilising existing currentness law;
- how to integrate deployment telemetry without creating hidden runtime truth;
- how to ensure agents cannot self-authorise deployment through tool chains;
- how to prevent conformance runners from becoming rubber stamps;
- how to handle secrets and signing keys without turning CP15 into a secrets-management product spec;
- how to keep CP15 from becoming generic CI/CD/MLOps law.

Open questions for later phases:

- should current/default promotion be represented as a CP15 contract or an addendum to existing currentness contracts;
- how much SBOM structure belongs in OFARM versus external references;
- which deployment surfaces require canary by default;
- what is the minimal acceptable rollback posture for high-consequence advisory-only surfaces;
- how model evaluation evidence should reference CP13 and CP14 artifacts;
- how to represent generated prompt/policy changes without exposing sensitive prompt content where redaction is required;
- whether CP15 should define a `SoftwareSupplyChainIncident` severity taxonomy or delegate severity to companion policy.

---

## 49. Acceptance gate

CP15 should not be accepted until these are true:

```text
[ ] RFC text preserves OFARM truth, current-state, twin, pack, output, agent, CP11, CP12, CP13, and CP14 boundaries.
[ ] Baseline patch text is controlled and addendum-style, not a rewrite.
[ ] Machine contracts are draft/non-default.
[ ] Deployment authorisation cannot be inferred from build/test/scan/conformance/canary/tool success.
[ ] Generated artifact provenance and agent-run linkage are explicit.
[ ] Deployment candidate lifecycle states cannot skip required evidence/authority states.
[ ] Runtime-surface release binding is explicit.
[ ] CP11/CP12/CP13/CP14 gate interactions are represented.
[ ] Current/default promotion is not automatic.
[ ] Security finding waivers are scoped, approved, evidence-linked, and expiry-aware.
[ ] Rollback/disable posture is explicit for high-consequence deployment.
[ ] Model deployment candidates cannot be authorised by CP13/CP14 evidence alone.
[ ] Prompt/policy/workflow changes cannot alter authority or high-consequence behaviour without governance.
[ ] Output qualification blocks production-readiness claims without evidence.
[ ] Conformance runner has positive and negative fixtures.
[ ] Steward validation passes after merge.
```

---

## 50. Phase 3 conclusion

CP15 should proceed to baseline patch planning.

The RFC establishes the correct boundary:

```text
agentic generation and delivery evidence may propose, test, qualify, and support review;
it does not deploy, promote, authorise, or certify by itself.
```

Next phase:

```text
CP15 Phase 4 — Baseline Patch Plan
```

The next phase should produce controlled addendum-style baseline patches only. It should not draft machine schemas yet and should not promote any draft/non-default schemas to current/default.


---

## Phase 7 final reconciliation addendum — 2026-05-30

This Phase 7 package reconciles the CP15 RFC draft with the CP15 hostile review and Phase 6.1 remediation. The amendment remains bounded to agentic software delivery and model deployment governance.

The following hardening decisions are now part of the CP15 final candidate package:

- deployment candidates must not advance on failed build, rejected SBOM, blocking dependency risk, blocking static/security findings, failed conformance, or unresolved deployment incidents;
- deployment plans must carry CP-gate, rollback, canary, environment-scope, and blast-radius posture where material;
- deployment authorization and promotion decisions require explicit authority trace, valid lifecycle state, temporal coherence, and compatible upstream evidence;
- release bundles require candidate, SBOM, conformance, signature, and runtime-surface consistency;
- runtime-surface bindings, runtime deployment receipts, canary results, rollback plans, waivers, incidents, and telemetry remain evidence/governance artifacts and do not create production readiness by themselves;
- model deployment candidates must not bypass CP13 learning-output gates or CP14 training/federated/model-improvement boundaries;
- generated prompt, policy, adapter, mapping, and workflow artifacts remain generated artifacts unless accepted through CP15 delivery gates;
- CP15 machine contracts remain draft/non-default and do not promote CP11, CP12, CP13, CP14, or CP15 schemas to current/default;
- CP15 does not claim production software-delivery readiness, production model-deployment readiness, generated-adapter readiness, cybersecurity certification, or autonomous release readiness.

The executable conformance lane for this candidate is:

```text
04_implementation_and_conformance/conformance_runners/agentic_software_delivery_model_deployment_conformance/ofarm_cp15_phase6_1_conformance_runner.py
```

The Phase 7 package preserves the CP15 invariant:

```text
Generated software, generated adapters, generated mappings, model improvements, prompt/workflow changes, build success, test success, security scan completion, conformance run completion, capability declaration, canary success, deployment telemetry, runtime receipt, or agent tool success do not create deployment authority, runtime authority, current/default promotion, mission authority, Compliance Twin fact, or production readiness by themselves.
```
