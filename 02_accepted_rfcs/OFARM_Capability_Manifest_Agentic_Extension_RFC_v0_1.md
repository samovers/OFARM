# OFARM Capability Manifest Agentic Extension RFC v0.1

Status: ACCEPTED_RFC
Accepted date: 2026-05-16
Controlled promotion phase: AAI-CP5
Authority role: accepted RFC below active baseline and above companion artifacts.

## Purpose

This RFC promotes a bounded agentic capability/tool manifest-honesty layer. It makes manifest and tool self-description inspectable, evidence-qualified, and subordinate to OFARM runtime enforcement.

## Scope

This RFC promotes the following active machine-contract families under `03_machine_contracts/schemas/agent_manifest/`:

- `AgentToolManifest`
- `AgentToolDescriptor`
- `AgentSupportSection`
- `AgenticCapabilityManifestOverlay`
- `AgentToolEffectClassification`
- `AgentToolApprovalRequirement`
- `AgentToolSemanticPrecondition`
- `AgentExternalCallPolicy`
- `AgentTraceRetentionPolicy`
- `RedactionAndPermissionLimitedResultPolicy`
- `AgentToolDeclaredHintSet`
- `AgentDataLearningPolicy`
- `AgentCapabilityReadinessClaimLimit`

## Normative rules

### 1. Manifest declaration is descriptive, not dispositive

A manifest, tool descriptor, capability overlay, declared hint, API catalog, external protocol card, model/tool profile, or vendor statement may describe capability. It does not grant authority, approve a tool call, satisfy evidence, activate a pack, promote an artifact, publish an output, attest, file a submission, or create governance success.

### 2. Tool success is not governance success

A tool may execute successfully while the OFARM governance outcome is deny, require review, require human approval, degrade to advisory, refuse output, or emit a blocked-action trace. Runtime and public surfaces must preserve this distinction.

### 3. Declared hints are untrusted until reconciled

Read-only, idempotent, safe, destructive, external-call, data-retention, or model-use hints are non-authoritative. They must be checked against active policy, side-effect classification, external-call policy, authority posture, result qualification, and observed runtime behavior.

### 4. Readiness claims require evidence and expiry

Every readiness claim must declare its status, evidence references, public-claim allowance, evidence threshold, and expiry. CP5 allows declared/static readiness claims; it does not allow runtime-passed, two-agent-compatible, production-ready, autonomous-compliance, world-model-ready, live-registry, legal-advice, or external-standard claims without later executed evidence and explicit promotion.

### 5. Side effects and data flow must be explicit

A tool descriptor must declare target twin/surface, effect class, input/output schema references and hashes, data classes in/out, authentication modes, required scopes, external-call posture, approval requirements, semantic preconditions, trace-retention expectations, redaction/permission-limited result policy, data-learning posture, known limitations, prohibited uses, and result-disposition limits where applicable.

### 6. Manifest conflict fails closed

If a manifest or descriptor conflicts with active baseline law, authority policy, evidence sufficiency, freshness, sharing/revocation, pack/context policy, output disposition, public-surface qualification, trace evidence, or observed runtime behavior, the operation must deny, require review, require human approval, or emit a qualified/blocked result according to policy.

### 7. Capability Manifest overlay is not an alternate authority path

An `AgenticCapabilityManifestOverlay` may link agent support, tool manifests, and readiness claims to a base Capability Manifest. It must not replace the base Capability Manifest, expand runtime authority, or bypass CP2, CP3, or CP4 gates.

## Non-claims

This RFC does not promote world-model runtime, `WorldModelRun`, `WorldModelState`, `ScenarioSpec`, `ScenarioResultSet`, `EvidenceNeed`, `ObservationRequest`, output assembly preview, autonomous compliance decisioning, runtime AI-agent readiness, two-agent compatibility, production readiness, live registry integration, legal advice, or external-standard readiness.

## Conformance expectations

A conforming implementation must be able to detect at least these hostile cases:

- manifest says read-only but the descriptor or observed behavior writes;
- manifest omits network egress that the tool can perform;
- readiness claim says runtime-passed without executed evidence;
- approval requirement is absent for state-affecting or high-consequence effect classes;
- declared hints contradict effect classification;
- permission-limited or redacted results can leak through summaries;
- data-learning posture is unspecified or overbroad;
- static manifest validation is presented as production/runtime readiness.
