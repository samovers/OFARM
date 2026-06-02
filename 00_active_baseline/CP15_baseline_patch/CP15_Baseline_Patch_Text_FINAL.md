# CP15 Phase 4 — Baseline Patch Plan

```text
Status: controlled baseline patch plan
Amendment: CP15 — Agentic Software Delivery and Model Deployment Governance
Baseline rewrite: no
Machine schemas: not drafted in this phase
Post-CP15 amendment: not started
Current/default schema promotion: not performed
Production software/model deployment readiness: not claimed
```

## 0. Patch objective

CP15 adds a bounded baseline layer for **agentic software delivery and model deployment governance**.

The patch objective is not to create a CI/CD product spec or MLOps implementation. The objective is to make OFARM's existing truth, authority, evidence, conformance, runtime-surface, pack, agent, and output laws apply explicitly to generated software, generated adapters, model deployment candidates, prompt/workflow changes, release bundles, runtime-surface bindings, canary/rollback paths, deployment incidents, and supply-chain evidence.

The central CP15 invariant is:

```text
Generated software, generated adapters, generated mappings, model improvements, prompt/workflow changes, build success, test success, security scan completion, conformance run completion, capability declaration, canary success, deployment telemetry, or agent tool success do not create deployment authority, runtime authority, current/default promotion, mission authority, Compliance Twin fact, or production readiness by themselves.

Deployment requires explicit CP15 delivery envelope, authority trace, provenance/SBOM/security/conformance evidence, applicable CP11/CP12/CP13/CP14 gates, runtime-surface binding, deployment authorization, rollback posture, output qualification, and conformance evidence.
```

CP15 must preserve these existing OFARM invariants:

```text
- assertion/history-first truth remains canonical;
- current state remains governed materialisation;
- Advisory Twin / Compliance Twin separation remains intact;
- pack/profile law remains default-fail for unsafe surfaces;
- authority remains explicit, scoped, time-bounded, and default-deny;
- public-operation, preflight/dry-run, and result-qualification law remains active;
- agent actorship and agent run traces remain provenance/authority inputs, not authority by themselves;
- CP11 charter gates, CP12 mission gates, CP13 learning gates, and CP14 intelligence gates are not bypassed by generated code or deployment tooling;
- CP15 does not promote any draft/non-default CP11, CP12, CP13, CP14, or CP15 schemas to current/default.
```

---

# 1. File: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`

## 1.1 Patch C15-C-1 — Add CP15 boundary after the CP14 baseline addendum

### Exact section to add or amend

Insert after the existing CP14 baseline addendum, or if the file contains only CP11–CP13 addenda and CP14 is present through patch files, insert after the latest controlled-promotion addendum:

```text
## CP15 Agentic Software Delivery and Model Deployment Governance baseline addendum — 2026-05-30
```

### Proposed normative text

```text
## CP15 Agentic Software Delivery and Model Deployment Governance baseline addendum — 2026-05-30

### CP15-C.1 Delivery-governance purpose and boundary

CP15 introduces **Agentic Software Delivery and Model Deployment Governance** as an OFARM constitutional boundary for generated software, generated adapters, generated semantic mappings, generated workflows, prompt/policy changes, model deployment candidates, release bundles, runtime-surface bindings, canary/rollback paths, deployment telemetry, and software-supply-chain incidents.

CP15 is delivery-governance law, not a CI/CD product specification, cloud topology, generic MLOps platform, cybersecurity certification, legal/security advice, or automatic deployment engine.

Generated software, generated adapters, generated mappings, model improvements, prompt/workflow changes, build success, test success, static-analysis success, security-scan completion, conformance-run completion, capability-manifest declaration, canary success, deployment telemetry, runtime-deployment receipt, or agent tool success do not create deployment authority, runtime authority, current/default promotion, mission authority, Compliance Twin fact, or production readiness by themselves.

Deployment requires explicit delivery-envelope governance, authority trace, provenance/SBOM/security/conformance evidence, applicable CP11/CP12/CP13/CP14 gates, runtime-surface binding, deployment authorization, rollback posture, output qualification, and conformance evidence.

### CP15-C.2 CP15 core concepts

CP15 recognises the following OFARM-owned delivery-governance concepts:

- **SoftwareDeliveryBoundary**
- **GeneratedSoftwareArtifact**
- **GeneratedPatchArtifact**
- **GeneratedAdapterArtifact**
- **GeneratedWorkflowArtifact**
- **GeneratedPromptOrPolicyArtifact**
- **SemanticMappingCandidate**
- **AdapterGenerationRequest**
- **BuildProvenance**
- **SBOMReference**
- **DependencyRiskAssessment**
- **StaticAnalysisResult**
- **SecurityScanResult**
- **SecurityFindingWaiver**
- **ConformanceTestPlan**
- **ConformanceRunReceipt**
- **DeploymentCandidate**
- **DeploymentPlan**
- **DeploymentAuthorization**
- **DeploymentPromotionDecision**
- **ReleaseBundle**
- **RuntimeSurfaceReleaseBinding**
- **CanaryPlan**
- **CanaryResult**
- **RollbackPlan**
- **RollbackEvent**
- **DeploymentTelemetryEnvelope**
- **RuntimeDeploymentReceipt**
- **ModelDeploymentCandidate**
- **ModelEvaluationEvidence**
- **PromptPolicyChangeCandidate**
- **WorkflowDeploymentCandidate**
- **SoftwareSupplyChainIncident**
- **DeploymentIncident**
- **DeploymentOutputQualification**

These concepts are delivery-governance shells. They do not create alternate truth stores, alternate authority stores, automatic current/default promotion, or production readiness.

### CP15-C.3 Generated artifacts are candidates, not runtime law

A generated artifact is not executable OFARM law merely because an agent produced it, a build succeeded, tests passed, a security scan found no blocking issue, or a reviewer viewed it.

Generated software, generated adapters, generated semantic mappings, generated workflows, generated prompts, and generated policies must resolve to explicit CP15 artifact classes and lifecycle states. They remain candidates until they pass applicable authority, provenance, security, conformance, pack/profile, runtime-surface, output-qualification, and deployment gates.

A generated adapter or semantic mapping candidate must not mutate OFARM core meaning, override external-standard boundary law, bypass pack/profile merge law, or convert lossy mappings into hidden truth.

### CP15-C.4 Delivery lifecycle and no-shortcut rule

CP15 separates at least the following stages:

- generated artifact;
- build provenance;
- SBOM/dependency/license/use-constraint assessment;
- static analysis and security scan;
- conformance test plan;
- conformance run receipt;
- deployment candidate;
- deployment plan;
- deployment authorization;
- release bundle;
- runtime-surface release binding;
- canary plan and canary result;
- deployment promotion decision;
- runtime deployment receipt;
- deployment telemetry;
- rollback event;
- deployment incident or software-supply-chain incident.

No later state is valid merely because an earlier state exists. A build artifact is not a deployment candidate by itself. A passed test is not deployment authorization. A canary result is not promotion. A runtime deployment receipt is not proof of safety, correctness, conformance, or production readiness by itself.

### CP15-C.5 Deployment authority and human-governed defaults

CP15 deployment-sensitive actions must be evaluated through explicit AuthorityActionClass law.

High-consequence CP15 actions are human-governed or human-approval-required by default unless a later accepted RFC explicitly narrows that rule for a low-risk class. These include, at minimum:

- approving a DeploymentAuthorization;
- approving a DeploymentPromotionDecision;
- promoting any schema, contract, pack, policy, prompt, workflow, adapter, model, or release bundle to current/default;
- approving a SecurityFindingWaiver for blocking or high-severity findings;
- approving deployment to a CP11/CP12/CP13/CP14-sensitive runtime surface;
- approving model deployment candidate release;
- approving rollback disablement or emergency rollback bypass;
- approving release of mission-adapter, farm-to-farm intelligence, sustainability-claim, farm-memory, or Compliance Twin-affecting code.

A software agent may prepare artifacts, generate candidates, run tests, collect evidence, package review bundles, perform preflight/dry-run where authorised, and report blocked actions. A software agent may not by default grant deployment authority, waive blocking security findings, promote current/default artifacts, or declare production readiness.

### CP15-C.6 Evidence, conformance, SBOM, and security gate

A CP15 DeploymentCandidate must declare the evidence required for its intended use class and runtime surface. Evidence may include build provenance, SBOM reference, dependency risk assessment, license/use-constraint assessment, static-analysis result, security-scan result, security-finding waiver where allowed, conformance test plan, conformance run receipt, runtime-surface binding, pack/profile compatibility, and applicable CP11/CP12/CP13/CP14 gate traces.

Evidence sufficiency is consequence-sensitive. Evidence sufficient for advisory sandbox deployment is not evidence sufficient for production, Compliance Twin, mission-adapter, cross-farm intelligence, sustainability-claim, current/default, or farmer-facing high-consequence deployment.

A ConformanceRunReceipt is evidence. It is not deployment authorization, production readiness, security certification, or current/default promotion by itself.

### CP15-C.7 Runtime-surface release binding

A release bundle must bind explicitly to the runtime surface on which it may operate. Runtime surfaces may include advisory sandbox, internal developer preview, farmer-facing advisory surface, Compliance Twin support surface, CP11 charter-sensitive surface, CP12 mission-adapter surface, CP13 learning/farm-memory surface, CP14 intelligence-sharing surface, public/export surface, or current/default contract/policy surface.

A release bundle authorised for one runtime surface must not silently operate on a stronger surface. Surface escalation requires explicit CP15 deployment authorization and applicable authority/evidence/conformance gates.

### CP15-C.8 Model, prompt, policy, and workflow deployment boundary

A model deployment candidate, prompt/policy change candidate, or workflow deployment candidate is not deployed, approved, trusted, or production-ready merely because it is derived from CP13 learning output, CP14 model-improvement signal, public model registry metadata, benchmark result, or agent-generated evaluation.

Model deployment requires model-evaluation evidence, intended-use and prohibited-use classification, runtime-surface binding, applicable CP11/CP12/CP13/CP14 gates, security/privacy/use-constraint review, deployment authorization, rollback posture, and output qualification.

A CP13 learning result or CP14 model-improvement signal may inform a model deployment candidate. It does not become deployment authority or model release approval.

### CP15-C.9 Canary, rollback, telemetry, and incident boundary

A canary plan or canary result may support deployment promotion review. It does not create deployment-promotion authority by itself.

Rollback posture is required for deployment candidates whose failure could affect high-consequence outputs, farm operational data, CP11 charter-sensitive outputs, CP12 mission paths, CP13 learning/farm-memory paths, CP14 cross-farm intelligence, Compliance Twin surfaces, or current/default artifact surfaces.

Deployment telemetry and runtime deployment receipts are evidence candidates. They do not create truth, compliance fact, conformance proof, security proof, or production readiness by themselves.

SoftwareSupplyChainIncident and DeploymentIncident records must be traceable, reviewable, and capable of triggering rollback, disablement, quarantine, evidence review, conformance re-run, or currentness downgrade where policy requires.

### CP15-C.10 Current/default promotion boundary

Current/default schema, contract, pack, profile, policy, model, prompt, workflow, adapter, release bundle, or runtime-surface binding promotion requires explicit currentness or deployment-promotion law.

CP15 does not promote CP11, CP12, CP13, CP14, or CP15 draft/non-default schemas to current/default. CP15 only defines the governance boundary for future promotion decisions.

### CP15-C.11 Interaction with CP11, CP12, CP13, and CP14

A deployment that affects CP11 charter-sensitive outputs, CP12 mission/command/adaptor surfaces, CP13 learning/farm-memory outputs, or CP14 cross-farm intelligence outputs must satisfy the relevant CP11, CP12, CP13, or CP14 gate in addition to CP15 gates.

CP15 does not replace those gates. It prevents generated software, model deployment, prompt changes, workflow changes, release bundles, or agent tooling from bypassing them.

### CP15-C.12 Deferrals and non-claims

CP15 does not create:

- a full CI/CD product specification;
- specific cloud/vendor deployment architecture;
- a generic MLOps platform;
- OFARM Social constitution;
- OFARM Exchange constitution;
- robot mission or command law;
- farm-to-farm intelligence law;
- production software-delivery readiness;
- production model-deployment readiness;
- cybersecurity certification;
- legal, security, compliance, privacy, insurance, or certification advice;
- automatic current/default schema promotion;
- autonomous release readiness.

CP15 remains implementation-directed with bounded debt until CP15 machine contracts, conformance fixtures, hostile review, implementation evidence, steward validation, security review, and pilot/runtime evidence exist.

### CP15-C.13 Minimum conformance baseline

A CP15-conforming implementation must be able to show, at minimum, that:

- generated artifacts cannot deploy without DeploymentAuthorization;
- build success does not create DeploymentAuthorization;
- security scan success does not create DeploymentAuthorization;
- conformance run success does not create DeploymentAuthorization;
- a blocking security finding cannot be waived without authorised waiver and trace;
- release bundles cannot bind silently to stronger runtime surfaces;
- canary success cannot promote deployment without DeploymentPromotionDecision;
- rollback posture is required for high-consequence deployment classes;
- runtime deployment receipt does not become conformance proof, truth, or production readiness;
- CP11, CP12, CP13, and CP14 gates cannot be bypassed by generated code, adapters, models, prompts, workflows, or deployment tooling;
- current/default promotion cannot occur without explicit promotion authority and currentness trace;
- agent tool success cannot become deployment authority.
```

### Reason

This patch makes CP15 visible as baseline law while keeping detailed schema and conformance mechanics in RFC/machine-contract layers.

### Interaction with existing law

This extends existing agentic AI, public-surface, capability-manifest, preflight/dry-run, authority, pack, and output-qualification law. It also preserves CP11–CP14 boundaries by requiring CP15 to respect those gates rather than replace them.

### Risk of contradiction

Medium if CP15 is treated as production CI/CD or model-deployment implementation law. Low if kept as delivery-governance law.

### Baseline or RFC?

Baseline should include the invariant, boundary, core concept recognition, authority defaults, no-shortcut rules, CP11–CP14 gate preservation, and non-claims. Detailed field definitions, event/state transitions, and schema validations remain RFC and draft/non-default machine-contract work.

### Migration note

Existing generated code, adapters, models, workflows, prompts, deployment tooling, or conformance artifacts should be treated as advisory/development artifacts unless explicitly mapped to CP15 classes and governed through CP15 gates.

### Conformance implication

Phase 5/6 must produce draft schemas and fixtures proving that generated artifacts, test success, security scans, conformance runs, canary results, deployment receipts, and agent tool success cannot bypass deployment authority or currentness promotion.

---

## 1.2 Patch C15-C-2 — Amend OFARM-owned semantic territory

### Exact section to add or amend

Amend:

```text
### 3.5 OFARM-owned semantic territory
```

Add bullets:

```text
- agentic software delivery and generated-artifact governance;
- generated adapter, semantic mapping, workflow, prompt, and policy candidate governance;
- build provenance, SBOM, dependency-risk, security-scan, conformance-run, waiver, and supply-chain evidence governance;
- deployment candidate, deployment plan, deployment authorization, release bundle, runtime-surface binding, canary, rollback, telemetry, and deployment-incident governance;
- model deployment candidate and model-evaluation evidence governance;
- current/default schema/contract/policy/release-bundle promotion boundary law.
```

### Proposed normative text

```text
CP15 adds delivery-governance semantics to OFARM-owned territory. These semantics govern how generated software and model-deployment candidates may become release candidates, deployment candidates, runtime-surface bindings, or current/default promotion candidates without bypassing existing OFARM truth, authority, evidence, conformance, pack/profile, output, agent, and CP11–CP14 laws.
```

### Reason

CP15 concepts affect OFARM runtime authority and currentness. They must not enter active meaning through a single tool, build pipeline, agent, deployment system, external registry, or adapter.

### Interaction with existing law

This follows the existing no-hidden-core rule and mirrors CP11–CP14 controlled concept promotion.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline concept recognition belongs here. Field-level detail remains in the CP15 RFC and draft schemas.

### Migration note

Legacy scripts, local builds, generated code, or implementation artifacts remain implementation/supporting material unless mapped through CP15 governance.

### Conformance implication

Generated-artifact and deployment-gate fixtures must show that no tool or agent creates hidden core semantics or runtime authority.

---

## 1.3 Patch C15-C-3 — Add CP15 artifact-family recognition

### Exact section to add or amend

Amend:

```text
### 5.2 Artifact families
```

Under decision/governance artifacts and interaction/exchange/runtime-support areas, add CP15 artifact families.

### Proposed normative text

```text
CP15 adds the following delivery-governance artifact families:

- generated software artifact;
- generated patch artifact;
- generated adapter artifact;
- generated workflow artifact;
- generated prompt or policy artifact;
- semantic mapping candidate;
- build provenance artifact;
- SBOM/dependency/security evidence artifact;
- conformance test plan and conformance run receipt;
- deployment candidate;
- deployment plan;
- deployment authorization;
- deployment promotion decision;
- release bundle;
- runtime-surface release binding;
- canary and rollback artifacts;
- deployment telemetry and runtime deployment receipt;
- model deployment candidate and model-evaluation evidence;
- prompt/policy/workflow deployment candidate;
- software-supply-chain incident and deployment incident;
- deployment output qualification.

These are delivery-governance artifacts. They do not become canonical domain truth, Compliance Twin fact, current-state materialisation, mission authority, farm-memory truth, cross-farm intelligence truth, or production readiness by existence alone.
```

### Reason

CP15 requires explicit artifact families so generated outputs are not handled as generic logs or untyped files.

### Interaction with existing law

It preserves artifact constitution and prevents a generic `AgentOutput` or `GeneratedOutput` bucket.

### Risk of contradiction

Low if no generic generated-output truth bucket is created.

### Baseline or RFC?

Baseline should recognise families. Lifecycle details remain RFC/schemas.

### Migration note

Existing generated implementation artifacts may be referenced as implementation material but are not CP15 artifacts until classified.

### Conformance implication

Conformance must reject deployment claims without typed CP15 artifact chain.

---

## 1.4 Patch C15-C-4 — Add CP15 pack/profile surface families

### Exact section to add or amend

Amend:

```text
### 6.6 Touched surfaces
### 6.7 Surface families
### 6.10 What packs may not change
### 6.13 Baseline family rules
```

### Proposed normative text

Add touched surfaces:

```text
- software-delivery policy;
- generated-artifact policy;
- semantic-mapping policy;
- adapter-generation policy;
- conformance-test policy;
- deployment-authorization policy;
- release-bundle policy;
- runtime-surface binding policy;
- canary/rollback policy;
- security-finding waiver policy;
- model-deployment policy;
- prompt/workflow deployment policy;
- current/default promotion policy.
```

Add `PackSurfaceFamily` values:

```text
- SOFTWARE_DELIVERY_POLICY
- GENERATED_ARTIFACT_POLICY
- SEMANTIC_MAPPING_POLICY
- ADAPTER_GENERATION_POLICY
- CONFORMANCE_TEST_POLICY
- DEPLOYMENT_AUTHORIZATION_POLICY
- RELEASE_BUNDLE_POLICY
- RUNTIME_SURFACE_BINDING_POLICY
- CANARY_ROLLBACK_POLICY
- SECURITY_WAIVER_POLICY
- MODEL_DEPLOYMENT_POLICY
- PROMPT_WORKFLOW_DEPLOYMENT_POLICY
- CURRENTNESS_PROMOTION_POLICY
```

Add to what packs may not change:

```text
A pack/profile must not:
- make generated software deployable by default;
- weaken CP15 deployment authorization requirements without explicit governance;
- turn conformance success, security-scan success, build success, canary success, or telemetry success into deployment authority;
- promote schemas, contracts, packs, models, prompts, workflows, or release bundles to current/default by pack activation alone;
- bypass CP11 charter gates, CP12 mission gates, CP13 learning gates, or CP14 intelligence gates;
- make external repositories, package registries, model registries, or vendor build systems hidden OFARM authority;
- waive blocking security findings without an authorised SecurityFindingWaiver and trace.
```

Add baseline family rules:

```text
- **SOFTWARE_DELIVERY_POLICY**: STRONGEST_REQUIREMENT for stricter gates; HARD_FAIL on incompatible deployment-authority posture.
- **GENERATED_ARTIFACT_POLICY**: STRONGEST_REQUIREMENT for stricter provenance/evidence requirements; HARD_FAIL on hidden-authority conflicts.
- **SEMANTIC_MAPPING_POLICY**: IDENTICAL_ONLY or HARD_FAIL for claim-bearing/high-consequence mapping equivalence; loss maps required for lossy mappings.
- **ADAPTER_GENERATION_POLICY**: STRONGEST_REQUIREMENT for stricter runtime-surface/authority gates; HARD_FAIL on CP11/CP12/CP13/CP14 bypass.
- **CONFORMANCE_TEST_POLICY**: STRONGEST_REQUIREMENT for stricter conformance; HARD_FAIL where conformance-result semantics conflict.
- **DEPLOYMENT_AUTHORIZATION_POLICY**: STRONGEST_REQUIREMENT or HARD_FAIL; weaker policy must not override stronger policy silently.
- **RELEASE_BUNDLE_POLICY**: STRONGEST_REQUIREMENT for signature, integrity, and evidence requirements; HARD_FAIL on conflicting runtime-surface binding.
- **RUNTIME_SURFACE_BINDING_POLICY**: HARD_FAIL on incompatible surface binding; weaker-to-stronger surface escalation requires explicit governance.
- **CANARY_ROLLBACK_POLICY**: STRONGEST_REQUIREMENT for stricter rollback/canary gates; HARD_FAIL where rollback requirements conflict.
- **SECURITY_WAIVER_POLICY**: STRONGEST_REQUIREMENT for waiver gates; HARD_FAIL where a pack would allow weaker high-severity waiver posture.
- **MODEL_DEPLOYMENT_POLICY**: STRONGEST_REQUIREMENT for model-evaluation, use-constraint, rollback, and runtime-surface gates; HARD_FAIL on deployment-authority conflict.
- **PROMPT_WORKFLOW_DEPLOYMENT_POLICY**: STRONGEST_REQUIREMENT for prompt/workflow gates; HARD_FAIL where hidden policy/runtime mutation would result.
- **CURRENTNESS_PROMOTION_POLICY**: STRONGEST_REQUIREMENT or HARD_FAIL; current/default promotion cannot be created by pack activation alone.
```

### Reason

CP15 delivery rules may vary by runtime surface, pack/profile, environment, deployment class, or policy set. Pack law must prevent weaker release policies from overriding stronger safety gates.

### Interaction with existing law

Extends pack-surface law without changing pack fundamentals.

### Risk of contradiction

Medium because deployment-policy pack surfaces are high-stakes. Mitigate by keeping machine-level merge checks draft/non-default until hostile review.

### Baseline or RFC?

Surface-family recognition and non-bypass rules belong in baseline; examples and merge fixtures belong in RFC/conformance.

### Migration note

Existing build/deployment scripts remain implementation artifacts. They do not become policy packs unless declared and governed.

### Conformance implication

Fixtures must cover weaker deployment-policy pack conflict, runtime-surface binding conflict, semantic-mapping loss, security-waiver conflict, and currentness-promotion bypass.

---

## 1.5 Patch C15-C-5 — Add CP15 authority action classes

### Exact section to add or amend

Insert after the current latest authority-action addendum, likely after CP14 authority action additions:

```text
### 7.10e CP15 software-delivery and model-deployment authority actions
```

### Proposed normative text

```text
### 7.10e CP15 software-delivery and model-deployment authority actions

CP15 adds software-delivery and model-deployment action classes. These must be evaluated through ordinary OFARM authority law. A broad role, model confidence, build success, tool success, security scan, conformance run, capability declaration, canary result, or deployment telemetry is not an AuthorityGrant.

CP15 recognised action classes include:

- **DELIVERY_REGISTER_GENERATED_ARTIFACT**
- **DELIVERY_APPROVE_GENERATED_ARTIFACT_FOR_REVIEW**
- **DELIVERY_APPROVE_SEMANTIC_MAPPING_CANDIDATE**
- **DELIVERY_APPROVE_ADAPTER_GENERATION_REQUEST**
- **DELIVERY_ACCEPT_BUILD_PROVENANCE**
- **DELIVERY_ACCEPT_SBOM_REFERENCE**
- **DELIVERY_ACCEPT_DEPENDENCY_RISK_ASSESSMENT**
- **DELIVERY_ACCEPT_STATIC_ANALYSIS_RESULT**
- **DELIVERY_ACCEPT_SECURITY_SCAN_RESULT**
- **DELIVERY_APPROVE_SECURITY_FINDING_WAIVER**
- **DELIVERY_APPROVE_CONFORMANCE_TEST_PLAN**
- **DELIVERY_ACCEPT_CONFORMANCE_RUN_RECEIPT**
- **DELIVERY_CREATE_DEPLOYMENT_CANDIDATE**
- **DELIVERY_APPROVE_DEPLOYMENT_PLAN**
- **DELIVERY_AUTHORIZE_DEPLOYMENT**
- **DELIVERY_APPROVE_RELEASE_BUNDLE**
- **DELIVERY_BIND_RUNTIME_SURFACE**
- **DELIVERY_APPROVE_CANARY_PLAN**
- **DELIVERY_ACCEPT_CANARY_RESULT**
- **DELIVERY_PROMOTE_DEPLOYMENT**
- **DELIVERY_APPROVE_ROLLBACK_PLAN**
- **DELIVERY_TRIGGER_ROLLBACK**
- **DELIVERY_ACCEPT_RUNTIME_DEPLOYMENT_RECEIPT**
- **DELIVERY_RECORD_DEPLOYMENT_TELEMETRY**
- **DELIVERY_RECORD_SOFTWARE_SUPPLY_CHAIN_INCIDENT**
- **DELIVERY_RECORD_DEPLOYMENT_INCIDENT**
- **DELIVERY_RESOLVE_DEPLOYMENT_INCIDENT**
- **DELIVERY_APPROVE_MODEL_DEPLOYMENT_CANDIDATE**
- **DELIVERY_APPROVE_PROMPT_POLICY_CHANGE**
- **DELIVERY_APPROVE_WORKFLOW_DEPLOYMENT**
- **DELIVERY_PROMOTE_CURRENT_DEFAULT_ARTIFACT**
- **DELIVERY_REVOKE_OR_QUARANTINE_RELEASE**

By default, deployment authorization, release-bundle approval, runtime-surface binding to high-consequence surfaces, high-severity security waiver approval, model deployment approval, prompt/policy/workflow deployment approval, rollback-bypass approval, and current/default promotion are human-governed or human-approval-required.

Software agents may generate candidates, collect evidence, run tests, draft deployment plans, prepare review packages, and report blocked actions under explicit authority envelopes. They may not by default authorise deployment, waive blocking findings, promote current/default artifacts, or declare production readiness.
```

### Reason

CP15 needs action-class specificity so generated software and deployment tooling cannot act under broad developer/agent roles.

### Interaction with existing law

This extends default-deny authority law and agent actorship law.

### Risk of contradiction

Low if actions are mapped in the Authority Action Matrix extension.

### Baseline or RFC?

Baseline should define the action family and human-governed defaults. Detailed matrix posture belongs to an RFC addendum.

### Migration note

Existing developer roles do not automatically receive CP15 high-governance rights.

### Conformance implication

Fixtures must prove agents cannot authorise deployment, waive blocking security findings, or promote current/default artifacts by tool success.

---

## 1.6 Patch C15-C-6 — Add deployment/currentness high-consequence rule

### Exact section to add or amend

Insert after the latest high-consequence use extension, likely after CP14 current-state/output boundary text:

```text
### 10.15e CP15 deployment and currentness high-consequence rule
```

### Proposed normative text

```text
### 10.15e CP15 deployment and currentness high-consequence rule

A CP15 deployment-sensitive action is high-consequence when it can affect:

- current/default schema, contract, pack, profile, policy, model, prompt, workflow, adapter, or release-bundle state;
- Compliance Twin surfaces;
- CP11 sustainability claims or charter-sensitive outputs;
- CP12 mission/command/robot/machine adapter paths;
- CP13 farm-memory, learning-promotion, or causal-estimate surfaces;
- CP14 cross-farm intelligence, training-use, regional alert, or benchmark surfaces;
- farmer-facing high-consequence outputs;
- public/export/partner-facing outputs;
- security, secrets, credentials, signing keys, or authority tokens;
- rollback, emergency-disable, quarantine, or incident-handling paths.

High-consequence CP15 actions require explicit authority, provenance, evidence sufficiency, conformance posture, runtime-surface binding, rollback posture, output qualification, and applicable CP11–CP14 gate evaluation.

A build result, scan result, conformance run, deployment receipt, telemetry stream, canary result, capability declaration, or generated summary is not current state, not deployment authority, not promotion authority, and not production readiness by itself.
```

### Reason

Deployment actions can alter runtime behaviour even when they do not directly mutate farm records. They must be treated as high-consequence when they affect governed surfaces.

### Interaction with existing law

This complements current high-consequence query/output/currentness law and no-shortcut promotion law.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline rule. Detailed use-class taxonomy remains RFC/schema work.

### Migration note

Implementation scripts and release processes need to declare which surface/use class they affect before CP15 gates apply.

### Conformance implication

Fixtures must reject high-consequence deployment without authority/evidence/conformance/runtime-surface/rollback basis.

---

## 1.7 Patch C15-C-7 — Add Advisory/Compliance boundary for delivery artifacts

### Exact section to add or amend

Insert after the latest Advisory/Compliance boundary addendum, likely after CP14 boundary text:

```text
### 12.9 CP15 delivery artifact twin boundary
```

### Proposed normative text

```text
### 12.9 CP15 delivery artifact twin boundary

Generated artifacts, deployment candidates, canary results, model-evaluation evidence, deployment telemetry, conformance run receipts, and software-supply-chain findings are delivery-governance evidence. They belong to Advisory or governance/workflow posture by default unless explicitly accepted into a stronger governed consequence through ordinary OFARM authority, review, evidence, currentness, and promotion law.

They may support review, block deployment, request evidence, trigger rollback, qualify outputs, or prepare promotion decisions.

They may not directly create Compliance Twin facts, accepted execution consequences, accepted sustainability claims, accepted farm-memory entries, accepted cross-farm intelligence facts, mission dispatch authority, current/default promotion, or production readiness.

A bridge from delivery evidence toward Compliance Twin consequence, current/default promotion, runtime-surface release, or production claim must pass CP15 deployment governance and any applicable CP11, CP12, CP13, or CP14 gates.
```

### Reason

Delivery evidence can be persuasive and machine-generated. It must not become hidden governance or compliance truth.

### Interaction with existing law

Preserves Advisory/Compliance and bridge rule.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline rule.

### Migration note

Existing CI logs and model-evaluation outputs should be treated as evidence candidates unless governed.

### Conformance implication

Fixtures must prove deployment telemetry and conformance run receipts do not auto-create Compliance Twin or current/default consequences.

---

## 1.8 Patch C15-C-8 — Add CP15 glossary entries

### Exact section to add or amend

Append to:

```text
## 17. Glossary
```

### Proposed normative text

```text
### SoftwareDeliveryBoundary
A governed boundary defining how generated artifacts, build/security/conformance evidence, deployment candidates, release bundles, runtime-surface bindings, canary/rollback paths, and deployment incidents may affect OFARM runtime surfaces.

### GeneratedSoftwareArtifact
A software artifact generated or materially modified by a software agent or agentic development process, without deployment authority by itself.

### GeneratedAdapterArtifact
A generated integration or adapter artifact that maps external inputs, outputs, APIs, schemas, or vendor systems into OFARM runtime surfaces, without source-of-meaning authority by itself.

### SemanticMappingCandidate
A proposed semantic mapping whose coverage, loss, authority, and conformance must be governed before high-consequence use.

### BuildProvenance
A record of build inputs, process, environment, toolchain, source refs, agent/run refs, and artifact digest sufficient to reconstruct or assess a build.

### SBOMReference
A reference to software bill of materials information relevant to dependency, license, use-constraint, and supply-chain risk.

### SecurityFindingWaiver
A governed waiver of a security finding, not a security proof, and not valid without authority, scope, expiry, and trace.

### ConformanceRunReceipt
A record of conformance execution and results. It is evidence, not deployment authorization.

### DeploymentCandidate
A proposed deployment unit awaiting authority, evidence, runtime-surface, rollback, and conformance gates.

### DeploymentAuthorization
A governed authorization allowing deployment under specified scope, time, environment, surface, evidence, and rollback constraints.

### DeploymentPromotionDecision
A governed decision promoting or refusing a deployment candidate or release bundle for a specified runtime surface or currentness class.

### ReleaseBundle
A packaged set of deployment artifacts, evidence, manifests, signatures, policies, rollback information, and runtime-surface bindings.

### RuntimeSurfaceReleaseBinding
A governed binding between a release bundle and an allowed OFARM runtime surface.

### CanaryResult
A bounded canary outcome record. It is evidence, not promotion by itself.

### RollbackPlan
A governed rollback or disablement plan for a deployment candidate or release bundle.

### RuntimeDeploymentReceipt
A runtime receipt indicating deployment occurrence or status. It is not production readiness or conformance proof by itself.

### ModelDeploymentCandidate
A proposed model release candidate requiring model-evaluation evidence, use constraints, runtime-surface binding, authority, rollback, and CP11–CP14 gate checks where applicable.

### DeploymentOutputQualification
The visible or machine-readable qualification required for deployment-related outputs, claims, dashboards, public surfaces, and agent answers.
```

### Reason

Glossary entries are needed because CP15 introduces baseline terms.

### Interaction with existing law

No conflict.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline glossary entries should be compact. Expanded definitions remain RFC/machine contracts.

### Migration note

Use exact names across RFC, schemas, companion artifact, and fixtures.

### Conformance implication

Schema names should align with glossary names.

---

# 2. File: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`

## 2.1 Patch C15-P-1 — Add CP15 delivery gate to runtime enforcement

### Exact section to add or amend

Insert after the existing CP14 runtime-enforcement addendum, or after the latest CP13/CP14 runtime addendum if CP14 is applied through patch files:

```text
## CP15 Agentic Software Delivery and Model Deployment Governance runtime-enforcement addendum — 2026-05-30
```

### Proposed normative text

```text
## CP15 Agentic Software Delivery and Model Deployment Governance runtime-enforcement addendum — 2026-05-30

### CP15-P.1 Delivery-sensitive runtime surface

A delivery-sensitive runtime surface is any OFARM runtime surface on which generated software, adapters, mappings, workflows, prompts, policies, model candidates, release bundles, runtime-surface bindings, canary/rollback mechanisms, or deployment tooling can affect governed outputs, current/default state, CP11 charter-sensitive paths, CP12 mission paths, CP13 learning/farm-memory paths, CP14 intelligence paths, Compliance Twin surfaces, public/export surfaces, security/credential/signing-token surfaces, or farmer-facing high-consequence behavior.

### CP15-P.2 Delivery governance gate

For delivery-sensitive use, the runtime must resolve the applicable SoftwareDeliveryBoundary and evaluate:

- artifact identity and lifecycle state;
- agent-generation provenance and agent-run trace;
- build provenance and artifact digest;
- SBOM/dependency/license/use-constraint posture;
- static-analysis and security-scan posture;
- security-finding waiver posture;
- conformance test plan and conformance run receipt;
- semantic mapping and adapter-generation evidence;
- runtime-surface release binding;
- deployment environment scope and blast radius;
- deployment authorization;
- rollback posture;
- canary posture where used;
- deployment promotion decision where promotion is requested;
- applicable CP11, CP12, CP13, and CP14 gate traces;
- output qualification and readiness/non-claim posture.

The gate must emit or link a CP15 delivery evaluation trace where the outcome affects deployment, refusal, qualification, review, promotion, rollback, quarantine, current/default promotion, or publication/export.

### CP15-P.3 Agentic development boundary

Software agents may generate artifacts, produce patches, propose semantic mappings, generate adapters, prepare workflows, run tests, gather evidence, draft release bundles, and prepare review packages where authorised.

Agent tool success, agent confidence, build success, test success, conformance success, security scan success, canary success, or deployment telemetry is not deployment authority, runtime authority, current/default promotion, or production readiness.

A software agent may not by default authorise deployment, waive blocking security findings, approve release bundles, promote current/default artifacts, bind release bundles to stronger runtime surfaces, approve rollback bypass, or declare production readiness.

### CP15-P.4 Deployment and runtime-surface binding

A deployment candidate must declare its runtime-surface target. A release bundle authorised for an advisory sandbox cannot silently run on farmer-facing, Compliance Twin, CP11 charter-sensitive, CP12 mission-adapter, CP13 learning/farm-memory, CP14 intelligence, public/export, or current/default surfaces.

Surface escalation requires explicit deployment authorization, runtime-surface release binding, authority trace, evidence/conformance basis, rollback posture, and output qualification.

### CP15-P.5 Current/default promotion gate

Current/default promotion for schemas, contracts, packs, profiles, policies, prompts, workflows, adapters, models, release bundles, or runtime-surface bindings requires explicit promotion authority and currentness trace.

A CP15 deployment path must not promote CP11, CP12, CP13, CP14, or CP15 draft/non-default schemas to current/default unless a separate currentness-promotion decision exists.

### CP15-P.6 Security, SBOM, dependency, and waiver gate

A high-consequence deployment candidate must expose SBOM, dependency-risk, license/use-constraint, static-analysis, security-scan, and waiver posture where applicable. A blocking or high-severity security finding cannot be waived without explicit SecurityFindingWaiver authority, scope, expiry, evidence, and review trace.

A waiver is not a security proof and does not remove the underlying finding from trace.

### CP15-P.7 Canary, rollback, telemetry, and incident gate

A canary result is evidence, not promotion. A rollback plan is required where deployment failure can affect high-consequence surfaces. Runtime deployment receipt and deployment telemetry are evidence candidates and must not become production readiness or conformance proof by themselves.

DeploymentIncident and SoftwareSupplyChainIncident must be capable of triggering rollback, quarantine, disablement, currentness downgrade, conformance rerun, evidence review, or human review where policy requires.

### CP15-P.8 Model, prompt, policy, and workflow deployment gate

ModelDeploymentCandidate, PromptPolicyChangeCandidate, and WorkflowDeploymentCandidate objects must be evaluated against intended-use, prohibited-use, evidence, security, privacy, runtime-surface, rollback, and CP11–CP14 gate requirements.

A CP13 learning result or CP14 model-improvement signal may support a candidate. It does not authorize deployment or model release.

### CP15-P.9 Output and readiness qualification

Deployment-facing outputs, agent answers, dashboards, generated summaries, release notes, model cards, public/export surfaces, and capability manifests must not imply deployment readiness, production readiness, security certification, model approval, current/default promotion, or conformance status stronger than the evidence and authority support.

A DeploymentOutputQualification or equivalent result qualification is required for high-consequence deployment-facing outputs.

### CP15-P.10 Runtime non-claims

Runtime support for CP15 remains implementation-directed with bounded debt until CP15 machine contracts, conformance fixtures, hostile review, implementation evidence, security review, steward validation, and pilot/runtime evidence exist.

CP15 runtime support does not claim production software-delivery readiness, production model-deployment readiness, cybersecurity certification, legal/security advice, automatic current/default promotion, autonomous release readiness, generic MLOps readiness, or full CI/CD product implementation.
```

### Reason

The Platform Runtime must know where CP15 gates occur. Otherwise CP15 remains a model-law statement without runtime effect.

### Interaction with existing law

This extends existing public-surface, preflight/dry-run, enforcement, agent, capability-manifest, and result-qualification law.

### Risk of contradiction

Medium if treated as runtime topology or CI/CD product law. Low if kept as enforcement-boundary law.

### Baseline or RFC?

Baseline runtime addendum should include gate posture and non-claims. Detailed schemas/runners remain below baseline.

### Migration note

Existing implementation build scripts may remain implementation artifacts; they are not CP15-governed release paths until classified as delivery-sensitive.

### Conformance implication

Conformance must show CP15 gates block deployment, promotion, runtime-surface escalation, and security waiver bypass.

---

## 2.2 Patch C15-P-2 — Amend EnforcementChain for delivery-sensitive paths

### Exact section to add or amend

Amend the existing enforcement-chain section or add a CP15 note under the CP15 runtime addendum.

### Proposed normative text

```text
For delivery-sensitive paths, the runtime EnforcementChain must include, where applicable:

1. generated-artifact and source/provenance normalization;
2. authority evaluation;
3. structural/semantic validation;
4. pack/profile/runtime-surface applicability;
5. CP11/CP12/CP13/CP14 gate evaluation where the deployment affects those surfaces;
6. SBOM/dependency/license/use-constraint evaluation;
7. static-analysis/security-scan evaluation;
8. conformance-test-plan and conformance-run evaluation;
9. security-waiver evaluation where findings are waived;
10. deployment-plan and environment-scope evaluation;
11. rollback/canary evaluation;
12. deployment authorization;
13. release-bundle/runtime-surface binding;
14. deployment-promotion decision where promotion is requested;
15. output/readiness qualification;
16. telemetry/receipt/incidents/rollback capture after deployment.
```

### Reason

This makes CP15 gates explicit without rewriting the platform architecture.

### Interaction with existing law

Additive. Does not remove existing enforcement steps.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline runtime extension.

### Migration note

Not every deployment path triggers every gate; gates are consequence-sensitive.

### Conformance implication

Fixtures must test high-consequence paths, low-risk advisory sandbox paths, and blocked escalation.

---

# 3. File: `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

## 3.1 Patch C15-A-1 — Add CP15 concept rows

### Exact section to add or amend

Add to:

```text
## 3. Register
```

or, if the register now uses active addenda for CP11–CP14, add:

```text
# OFARM Alignment Register CP15 update — accepted/merged baseline addendum
```

### Proposed normative text

```text
# OFARM Alignment Register CP15 update — baseline patch candidate

| Concept | Domain | Alignment class | External anchor posture | Canonical OFARM name | Rationale |
|---|---|---|---|---|---|
| SoftwareDeliveryBoundary | Software Delivery / Runtime Governance | OFARM_OWNED | External CI/CD and MLOps systems as integration surfaces only | SoftwareDeliveryBoundary | OFARM needs explicit delivery-governance boundary so generated artifacts and model deployments cannot bypass authority, evidence, conformance, runtime-surface, and CP11–CP14 gates. |
| GeneratedSoftwareArtifact | Software Delivery | OFARM_OWNED | Source-control and build tools as evidence sources only | GeneratedSoftwareArtifact | OFARM needs generated software to be typed as candidate artifact, not hidden runtime law. |
| GeneratedPatchArtifact | Software Delivery | OFARM_OWNED | Patch/diff tools as evidence sources only | GeneratedPatchArtifact | OFARM needs generated patches to remain reviewable candidates. |
| GeneratedAdapterArtifact | Interoperability / Runtime | OFARM_OWNED | Vendor APIs/adapters as external surfaces only | GeneratedAdapterArtifact | OFARM needs adapter generation governed so mappings do not mutate meaning or bypass runtime gates. |
| GeneratedWorkflowArtifact | Runtime / Agentic Development | OFARM_OWNED | Workflow engines as implementation surfaces only | GeneratedWorkflowArtifact | OFARM needs workflow changes governed where they affect OFARM outputs or actions. |
| GeneratedPromptOrPolicyArtifact | AI Runtime / Policy | OFARM_OWNED | Prompt tools/policy engines as implementation surfaces only | GeneratedPromptOrPolicyArtifact | OFARM needs prompt/policy changes governed where they alter runtime behavior or outputs. |
| SemanticMappingCandidate | Interoperability / Semantics | OFARM_OWNED | External standards/mappings as anchors only | SemanticMappingCandidate | OFARM needs candidate mappings to preserve loss/currentness/source-of-meaning boundaries. |
| BuildProvenance | Software Supply Chain | OFARM_OWNED | SLSA/SBOM/provenance standards as anchors only | BuildProvenance | OFARM needs build evidence without making build success deployment authority. |
| SBOMReference | Software Supply Chain | PROFILE_EXTERNAL | SBOM standards as profile anchors | SBOMReference | OFARM needs SBOM evidence while avoiding tool-specific lock-in. |
| DependencyRiskAssessment | Software Supply Chain / Security | OFARM_OWNED | Security tools as evidence sources only | DependencyRiskAssessment | OFARM needs dependency/license/use-constraint risk posture. |
| StaticAnalysisResult | Software Supply Chain / Security | OFARM_OWNED | Static analysis tools as evidence sources only | StaticAnalysisResult | OFARM needs static-analysis evidence without treating tool success as authority. |
| SecurityScanResult | Software Supply Chain / Security | OFARM_OWNED | Security scanners as evidence sources only | SecurityScanResult | OFARM needs security scan evidence without security-certification claims. |
| SecurityFindingWaiver | Authority / Security | OFARM_OWNED | Governance/security review standards as anchors | SecurityFindingWaiver | OFARM needs governed waivers with scope, expiry, authority, and trace. |
| ConformanceTestPlan | Conformance | OFARM_OWNED | Test frameworks as implementation surfaces only | ConformanceTestPlan | OFARM needs declared conformance plans for deployment-sensitive paths. |
| ConformanceRunReceipt | Conformance | OFARM_OWNED | Test runners as evidence sources only | ConformanceRunReceipt | OFARM needs conformance-run evidence without treating test success as deployment authority. |
| DeploymentCandidate | Runtime Governance | OFARM_OWNED | CI/CD systems as implementation surfaces only | DeploymentCandidate | OFARM needs explicit deployment candidates before deployment authorization. |
| DeploymentPlan | Runtime Governance | OFARM_OWNED | Deployment systems as implementation surfaces only | DeploymentPlan | OFARM needs scope/blast-radius/rollback-aware deployment plans. |
| DeploymentAuthorization | Authority / Runtime Governance | OFARM_OWNED | External approval systems as evidence wrappers only | DeploymentAuthorization | OFARM needs explicit authority for deployment. |
| DeploymentPromotionDecision | Authority / Runtime Governance | OFARM_OWNED | Release management systems as evidence wrappers only | DeploymentPromotionDecision | OFARM needs explicit promotion decisions separate from test/canary success. |
| ReleaseBundle | Runtime Governance | OFARM_OWNED | Package registries as evidence/storage surfaces only | ReleaseBundle | OFARM needs governed bundles with evidence, signatures, runtime bindings, and rollback posture. |
| RuntimeSurfaceReleaseBinding | Runtime Governance | OFARM_OWNED | Deployment topology as implementation detail | RuntimeSurfaceReleaseBinding | OFARM needs binding from release bundles to allowed runtime surfaces. |
| CanaryPlan | Runtime Governance | OFARM_OWNED | Observability/canary tools as implementation surfaces only | CanaryPlan | OFARM needs bounded canary posture without treating canary success as promotion. |
| CanaryResult | Runtime Governance / Evidence | OFARM_OWNED | Observability tools as evidence sources only | CanaryResult | OFARM needs canary evidence. |
| RollbackPlan | Runtime Governance | OFARM_OWNED | Deployment tools as implementation surfaces only | RollbackPlan | OFARM needs rollback readiness for high-consequence deployments. |
| RollbackEvent | Runtime Governance / Event | OFARM_OWNED | Deployment tools as evidence sources only | RollbackEvent | OFARM needs rollback events as traceable governance artifacts. |
| DeploymentTelemetryEnvelope | Runtime Governance / Evidence | OFARM_OWNED | Observability tools as evidence sources only | DeploymentTelemetryEnvelope | OFARM needs telemetry evidence without production-readiness implication. |
| RuntimeDeploymentReceipt | Runtime Governance / Evidence | OFARM_OWNED | Deployment tools as evidence sources only | RuntimeDeploymentReceipt | OFARM needs deployment occurrence receipts without making them conformance proof. |
| ModelDeploymentCandidate | Model Governance | OFARM_OWNED | Model registries as external sources only | ModelDeploymentCandidate | OFARM needs model deployment governance without generic MLOps law. |
| ModelEvaluationEvidence | Model Governance / Evidence | OFARM_OWNED | Model cards/benchmarks as evidence anchors only | ModelEvaluationEvidence | OFARM needs model evaluation evidence without deployment authority. |
| PromptPolicyChangeCandidate | AI Runtime / Policy | OFARM_OWNED | Prompt/policy tools as implementation surfaces only | PromptPolicyChangeCandidate | OFARM needs prompt/policy changes governed where they affect outputs/actions. |
| WorkflowDeploymentCandidate | Runtime Governance | OFARM_OWNED | Workflow engines as implementation surfaces only | WorkflowDeploymentCandidate | OFARM needs workflow deployment candidates governed explicitly. |
| SoftwareSupplyChainIncident | Security / Runtime Governance | OFARM_OWNED | Security incident taxonomies as anchors only | SoftwareSupplyChainIncident | OFARM needs governed supply-chain incidents. |
| DeploymentIncident | Runtime Governance / Security | OFARM_OWNED | Incident systems as evidence sources only | DeploymentIncident | OFARM needs governed deployment incidents that can trigger rollback/quarantine. |
| DeploymentOutputQualification | Output / Runtime Governance | OFARM_OWNED | Result-qualification foundations only | DeploymentOutputQualification | OFARM needs deployment-facing outputs to disclose readiness, evidence, authority, limitation, and allowed/prohibited use posture. |

CP15 concepts are OFARM-owned because they govern how generated artifacts, software delivery, model deployment, runtime-surface binding, and currentness/promotion boundaries interact with OFARM truth, authority, evidence, conformance, pack, agent, output, and CP11–CP14 laws.

CP15 does not promote any CP11, CP12, CP13, CP14, or CP15 draft/non-default schema to current/default. CP15 does not create production software-delivery readiness, production model-deployment readiness, cybersecurity certification, generic MLOps readiness, or full CI/CD product implementation.
```

### Reason

CP15 terms must be listed as OFARM-owned/controlled so external CI/CD, registries, MLOps tools, or agents do not define them implicitly.

### Interaction with existing law

Matches CP11–CP14 alignment addenda pattern.

### Risk of contradiction

Low.

### Baseline or RFC?

Alignment Register baseline.

### Migration note

Existing implementation files are not automatically CP15 concepts.

### Conformance implication

Schema names and conformance fixtures should match these canonical names.

---

# 4. File: `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

## 4.1 Patch C15-R-1 — Add readiness and claim-limit addendum

### Exact section to add or amend

Append after the latest CP14 readiness addendum:

```text
## CP15 Agentic Software Delivery and Model Deployment Governance readiness and claim-limit addendum — 2026-05-30
```

### Proposed normative text

```text
## CP15 Agentic Software Delivery and Model Deployment Governance readiness and claim-limit addendum — 2026-05-30

### Readiness posture

CP15 improves OFARM by adding bounded model/runtime governance for agentic software delivery and model deployment. It is a governance closure, not a production software-delivery platform, model-deployment platform, MLOps platform, cybersecurity certification, or CI/CD implementation.

The package remains **implementation-directed with bounded debt**.

### Evidence currently available

CP15 currently provides or proposes:

- a CP15 RFC;
- controlled baseline patch text;
- alignment register updates;
- authority/action/event/pack addendum requirements;
- draft/non-default machine-contract candidates to be developed later;
- conformance fixture requirements to be developed later.

This is design and governance evidence. It is not production deployment evidence, cybersecurity-certification evidence, live runtime deployment evidence, model-performance validation, legal/security advice, or pilot/farmer validation.

### Claims allowed after CP15 baseline acceptance

After CP15 is accepted and reconciled, the package may claim:

- bounded model-law support for agentic software delivery and model deployment governance;
- explicit separation of generated artifacts, build evidence, security evidence, conformance evidence, deployment candidates, deployment authorization, release bundles, runtime-surface bindings, canary/rollback, deployment telemetry, and promotion decisions;
- explicit baseline hooks preventing generated artifacts, test success, scan success, conformance success, canary success, telemetry, or agent tool success from becoming deployment authority or current/default promotion by themselves;
- explicit preservation of CP11, CP12, CP13, and CP14 gates in delivery-sensitive paths.

### Claims still blocked after CP15

The package must not claim:

- production software-delivery readiness;
- production model-deployment readiness;
- autonomous release readiness;
- cybersecurity certification;
- legal/security/compliance/privacy/certification advice;
- full CI/CD product implementation;
- generic MLOps readiness;
- cloud/vendor deployment architecture readiness;
- automatic current/default schema promotion;
- CP11/CP12/CP13/CP14/CP15 draft schema promotion;
- mission authority through generated adapters;
- farm-to-farm intelligence deployment authority;
- OFARM Social or OFARM Exchange constitution.

### Evidence required before stronger claims

Stronger CP15 claims require:

- accepted CP15 draft/non-default machine contracts;
- executable CP15 conformance runners and fixtures;
- cross-record validation proving deployment authority cannot be created by build/test/scan/conformance/canary/tool success;
- runtime logs showing CP15 gates in delivery-sensitive paths;
- security review of CP15 evidence and waiver posture;
- runtime-surface binding tests;
- rollback/canary/incident fixtures;
- CP11/CP12/CP13/CP14 gate integration tests;
- steward validation of package currentness and non-claims.
```

### Reason

CP15 can be overclaimed easily because deployment tooling looks operationally powerful. Readiness/non-claims must be explicit.

### Interaction with existing law

Matches CP11–CP14 readiness posture.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline readiness posture.

### Migration note

No implementation readiness changes until conformance and hostile review complete.

### Conformance implication

Capability manifests must distinguish CP15 conceptual support from runtime implementation support.

---

# 5. File: `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

## 5.1 Patch C15-H-1 — Add hostile-review update

### Exact section to add or amend

Append after the latest CP14 hostile-review update:

```text
## CP15 Agentic Software Delivery and Model Deployment Governance hostile-review addendum — 2026-05-30
```

### Proposed normative text

```text
## CP15 Agentic Software Delivery and Model Deployment Governance hostile-review addendum — 2026-05-30

### Hostile-reader verdict

CP15 is a necessary governance extension if OFARM is to operate in a future where agents generate software, adapters, mappings, workflows, prompts, policies, and model deployments.

A hostile reader should not treat CP15 as production software-delivery readiness, model-deployment readiness, cybersecurity certification, or an MLOps/CI-CD product implementation.

### Closed or substantially reduced by CP15

CP15 closes or reduces these conceptual gaps:

- generated software is no longer an untyped implementation side-effect;
- generated adapters and semantic mappings are governed candidates rather than hidden source-of-meaning changes;
- build success, test success, security scan success, conformance run success, canary success, deployment receipt, and telemetry are separated from deployment authority;
- security waivers require governed authority rather than informal override;
- release bundles and runtime-surface bindings become explicit;
- deployment authorization and deployment promotion decisions are separated;
- model deployment candidates require model-evaluation evidence and use constraints;
- CP13 learning output and CP14 model-improvement signals cannot become model deployment authority;
- CP11, CP12, CP13, and CP14 gates remain active for deployment-sensitive paths;
- current/default promotion remains governed and separate from deployment tooling.

### Still open and hostile-reader relevant

CP15 does not close:

- production CI/CD implementation;
- cloud/vendor deployment topology;
- generic MLOps implementation;
- cybersecurity certification;
- legal/security/privacy/compliance advice;
- real-world runtime deployment evidence;
- model performance validation in production;
- supply-chain security assurance;
- live rollback/canary proof;
- human/operator UX for release governance;
- current/default schema promotion;
- CP11/CP12/CP13/CP14 draft-schema currentness promotion.

### Hostile-reader risks after CP15

The main CP15 failure modes are:

- agent-generated code being treated as deployable because it compiles;
- conformance success being mistaken for deployment authority;
- security scan success being mistaken for security certification;
- canary success being mistaken for promotion authority;
- runtime deployment receipt being mistaken for production readiness;
- model-improvement signals becoming model deployment without review;
- semantic mappings weakening OFARM meaning;
- generated adapters bypassing CP11/CP12/CP13/CP14 gates;
- current/default promotion occurring through release tooling rather than governance.

### Hostile-review conclusion

CP15 should proceed only if it remains a delivery-governance amendment. It must not become a product implementation, CI/CD/MLOps platform, automatic release engine, legal/security certification framework, or currentness promotion shortcut.

### CP15 exact non-claim wording — 2026-05-30

CP15 does not claim production software-delivery readiness, production model-deployment readiness, autonomous release readiness, cybersecurity certification, legal/security/compliance/privacy/certification advice, full CI/CD product implementation, generic MLOps readiness, cloud/vendor deployment architecture readiness, automatic current/default schema promotion, CP11/CP12/CP13/CP14/CP15 draft schema promotion, mission authority through generated adapters, farm-to-farm intelligence deployment authority, OFARM Social constitution, or OFARM Exchange constitution.
```

### Reason

The hostile-review memo must record what CP15 improves and what it does not close.

### Interaction with existing law

Matches the established hostile-review posture for CP11–CP14.

### Risk of contradiction

Low.

### Baseline or RFC?

Baseline hostile-review posture.

### Migration note

Use this as hostile-review baseline for Phase 6.

### Conformance implication

Hostile review should specifically attack generated-code authority, deployment-authority shortcuts, schema-promotion shortcuts, and CP11–CP14 bypass.

---

# 6. Summary of patch decisions

| File | Patch | Baseline now? | Remain RFC/detail? | Risk |
|---|---:|---:|---:|---|
| Constitution | CP15 boundary and invariant | Yes | Details in RFC | Low/medium |
| Constitution | CP15 concept recognition | Yes | Field definitions in RFC/schemas | Low |
| Constitution | Artifact-family recognition | Yes | Lifecycle in RFC/schemas | Low |
| Constitution | Pack/profile surfaces | Yes | Merge fixtures in conformance | Medium |
| Constitution | Authority action classes | Yes | Matrix addendum details | Low/medium |
| Constitution | High-consequence deployment/currentness rule | Yes | Use-class taxonomy in RFC/schemas | Low |
| Constitution | Advisory/Compliance boundary for delivery evidence | Yes | Bridge details in RFC | Low |
| Constitution | Glossary entries | Yes | Expanded definitions in RFC | Low |
| Platform Runtime | CP15 runtime gate | Yes | Schema/runtime implementation later | Medium |
| Platform Runtime | EnforcementChain extension | Yes | Detailed runner later | Low/medium |
| Alignment Register | CP15 concept rows | Yes | None | Low |
| Readiness Memo | CP15 readiness/non-claims | Yes | Evidence thresholds later | Low |
| Hostile Review | CP15 hostile-review update | Yes | Phase 6 hostile review later | Low |

---

# 7. Migration plan

Recommended migration order:

```text
1. Keep CP15 RFC as draft candidate until Phase 5/6 hardening.
2. Apply CP15 baseline patch text only after machine-contract implications and hostile review are available.
3. Add Alignment Register CP15 concept rows after confirming canonical names in Phase 5.
4. Add readiness and hostile-review addenda with exact non-claims.
5. Create CP15 draft/non-default machine contracts.
6. Create CP15 executable conformance fixtures.
7. Hostile-review CP15.
8. Harden schemas/conformance.
9. Final acceptance gate.
10. Only then consider merge as controlled amendment.
```

Do not promote any CP15 schemas or existing CP11–CP14 draft/non-default schemas to current/default during this process.

---

# 8. Conformance implications to carry into Phase 5/6

Minimum CP15 conformance families:

```text
generated_artifact_does_not_authorize_deployment
build_success_does_not_authorize_deployment
security_scan_success_does_not_authorize_deployment
conformance_run_success_does_not_authorize_deployment
canary_success_does_not_promote_deployment
runtime_deployment_receipt_not_production_readiness
agent_tool_success_not_deployment_authority
blocking_security_finding_requires_authorized_waiver
security_waiver_requires_scope_expiry_authority_trace
release_bundle_without_runtime_surface_binding_fails
runtime_surface_escalation_without_authorization_fails
high_consequence_deployment_without_rollback_plan_fails
cp11_sensitive_deployment_without_charter_gate_fails
cp12_mission_adapter_without_mission_gate_fails
cp13_learning_model_deployment_without_learning_gate_fails
cp14_model_improvement_signal_without_training_use_gate_fails
semantic_mapping_loss_without_loss_map_fails
adapter_generation_bypass_of_core_meaning_fails
model_deployment_candidate_without_model_evaluation_fails
prompt_policy_change_without_authority_fails
workflow_deployment_without_conformance_fails
current_default_promotion_without_currentness_trace_fails
```

---

# 9. Phase 4 conclusion

CP15 should proceed to Phase 5.

The patch is correctly bounded if it does only this:

```text
- makes agentic software delivery and model deployment governance visible in baseline law;
- adds CP15 concepts to the Alignment Register;
- adds delivery-sensitive runtime gate posture;
- extends authority, pack, output, Advisory/Compliance, currentness, and high-consequence rules to deployment-sensitive use;
- preserves CP11, CP12, CP13, and CP14 gates;
- preserves all non-claims;
- does not create CI/CD/MLOps product law;
- does not promote any draft/non-default schema to current/default.
```

Recommended next command:

```text
Start CP15 Phase 5.

Create the CP15 machine-contract plan.

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
- relation to CP12 mission/robot/command-adapter gates;
- relation to CP13 learning/farm-memory and model-improvement boundaries;
- relation to CP14 cross-farm/training-use/model-improvement boundaries;
- relation to deployment authority/currentness promotion;
- relation to security/SBOM/conformance/rollback evidence;
- conformance tests;
- examples.

Then produce draft schema-style definitions in OFARM-compatible form.

Do not promote CP11, CP12, CP13, CP14, or CP15 draft/non-default schemas to current/default.
Do not create OFARM Social, OFARM Exchange, public benchmark product, generic MLOps product, or cloud/vendor CI/CD implementation contracts.
Do not claim production software-delivery or model-deployment readiness.
```


---

# CP15 Phase 7 reconciliation note — 2026-05-30

The CP15 baseline patch is carried forward as a controlled addendum only. Phase 7 does not rewrite the Constitution or Platform Runtime.

The Phase 6.1 hostile-review remediation is incorporated by reference into the CP15 baseline patch posture:

```text
- deployment authorization remains separate from generated artifact state, build success, scan success, conformance success, canary success, runtime receipt, telemetry, and agent tool success;
- current/default schema or contract promotion remains outside CP15 draft schema staging and requires a separate currentness-promotion decision;
- model deployment remains separate from CP13 learning outputs and CP14 model-improvement or training-use signals;
- generated mission adapters or robot/machine-facing deployment surfaces must respect CP12 gates and do not create mission authority;
- sustainability-sensitive deployment surfaces must respect CP11 gates;
- CP15 machine contracts remain draft/non-default until formal currentness promotion;
- CP15 does not claim production software-delivery, model-deployment, generated-adapter, cybersecurity, or autonomous release readiness.
```
