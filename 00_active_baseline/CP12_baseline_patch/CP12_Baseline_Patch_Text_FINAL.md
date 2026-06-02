# CP12 Phase 4 — Baseline Patch Plan

Date: 2026-05-28  
Status: final CP12 baseline patch candidate; controlled patch text, not automatic merge  
Input: `02_accepted_rfcs/OFARM_Cyber_Physical_Mission_Envelope_RFC_v0_1.md` draft candidate  
Scope: baseline patch text only. No machine schemas. No CP13, CP14, or CP15 law.

---

## 0. Phase 4 verdict

CP12 should proceed as a bounded baseline extension.

The correct baseline move is to add a **Cyber-Physical Mission Envelope** layer to OFARM model/runtime law without turning OFARM into a robotics product specification or vendor control protocol.

The baseline patch should establish one invariant:

```text
Physical mission authority is not produced by recommendation, plan, preflight success, CP11 charter pass, agent confidence, tool invocation success, machine capability declaration, command acknowledgement, telemetry receipt, or adapter output alone.

Mission dispatch requires explicit CP12 mission envelope, authority trace, safety envelope, command integrity, and applicable preflight/current-state/charter gates.
```

CP12 should remain mission-envelope law. It should not produce full robot autonomy, fleet optimisation, vendor protocol law, safety certification, learning/farm-memory law, farm-to-farm intelligence law, generated-software deployment law, or livestock-specific law.

---

## 1. File: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`

### 1.1 Patch C12-C-1 — Add CP12 constitutional boundary

#### Exact section to add or amend

Append after the existing section:

```text
## CP11 Sustainable Autonomous Farming Charter baseline addendum — 2026-05-21
```

specifically after `### CP11-C.11 Non-claims`.

#### Proposed normative text

```text
## CP12 Cyber-Physical Mission Envelope baseline addendum — 2026-05-28

Status: CP12 baseline-law harmonisation candidate, pending acceptance of `OFARM_Cyber_Physical_Mission_Envelope_RFC_v0_1.md` and later machine-contract/conformance review.

This addendum introduces a bounded cyber-physical mission-envelope layer into OFARM model law. It is a controlled extension. It does not replace the Constitution, does not create a second truth model, does not alter assertion/history-first authority, does not promote current-state materialisations into deeper truth, does not collapse Advisory Twin and Compliance Twin, does not weaken CP11 charter gates, and does not make software agents physical governors.

CP12 defines the constitutional boundary between:

- advisory recommendation;
- planned intervention;
- mission candidate;
- mission plan;
- preflight or dry-run result;
- dispatch authorisation;
- command envelope;
- command acknowledgement;
- telemetry;
- execution receipt;
- mission verification;
- accepted execution consequence.

A recommendation, plan, preflight pass, CP11 charter pass, agent confidence, tool invocation success, machine capability declaration, command acknowledgement, telemetry receipt, or adapter output is not physical mission authority by itself.

### CP12-C.1 Mission-envelope purpose and boundary

A cyber-physical mission is any OFARM-governed preparation, dispatch, monitoring, receipt, verification, or incident handling path involving a physical actor that may move, sense, actuate, apply an input, affect a field/crop/zone, interact with a human/animal/environment, or create machine-reported evidence for a physical operation.

CP12 mission-envelope law applies to crop-farming contexts already within the active OFARM release boundary. It includes robots, drones, tractors, implements, actuators, irrigation devices, scouting devices, or other physical actors only to the extent they are represented through mission-envelope concepts. CP12 is not a vendor protocol and is not a safety certification.

The mission-envelope layer governs:

- mission identity and lifecycle;
- mission stage separation;
- mission authority actions;
- mission preflight and no-side-effect dry-run boundaries;
- current-state freshness for mission dispatch;
- CP11 charter precondition interaction;
- geofence, no-go-zone, route, and geometry-basis law;
- execution-window and temporal-coherence law;
- mission safety constraints;
- physical actor capability and compatibility;
- mission-specific autonomy levels;
- emergency stop, human override, local fallback, lost-link fallback, and remote takeover posture;
- command envelope, command signature, command expiry, and replay protection;
- mission dispatch authorisation;
- agent mission-preparation boundaries;
- Advisory Twin mission simulation boundaries;
- telemetry and execution-receipt truth boundaries;
- mission verification and accepted execution consequences;
- abort, emergency-stop, fallback, remote-takeover, near-miss, and physical-safety incident handling;
- vendor/machinery/robot/drone/tasking payload boundaries;
- mission outputs and reporting surfaces.

### CP12-C.2 CP12 core concepts

The following CP12 concepts are baseline-recognised OFARM-governed concepts and must be represented in the Alignment Register before they are treated as constitutional core:

- `CyberPhysicalMissionEnvelope`;
- `MissionIntent`;
- `MissionCandidate`;
- `MissionPlan`;
- `MissionScope`;
- `MissionLifecycleState`;
- `MissionPreflightTrace`;
- `MissionDispatchAuthorization`;
- `CommandEnvelope`;
- `CommandSignature`;
- `CommandAcknowledgement`;
- `ExecutionWindow`;
- `GeoFence`;
- `NoGoZone`;
- `RouteConstraint`;
- `MissionGeometryBasis`;
- `MissionSafetyConstraint`;
- `PhysicalActorCapabilityProfile`;
- `RobotCapabilityProfile`;
- `MachineCapabilityProfile`;
- `AutonomyLevelDeclaration`;
- `EmergencyStopPolicy`;
- `HumanOverridePolicy`;
- `LocalFallbackPolicy`;
- `LostLinkPolicy`;
- `RemoteTakeoverEvent`;
- `MissionTelemetryEnvelope`;
- `MissionExecutionReceipt`;
- `MissionVerification`;
- `MissionAbortEvent`;
- `NearMissEvent`;
- `PhysicalSafetyIncident`;
- `MissionOutputQualification`.

These concepts may be detailed by accepted RFCs, companion artifacts, machine contracts, examples, and conformance fixtures. They may not be introduced silently through a vendor adapter, robot app, machinery payload, AI tool result, telemetry stream, output template, or pack.

### CP12-C.3 Mission stage separation

OFARM distinguishes at least the following mission stages:

1. mission intent;
2. mission candidate;
3. mission plan;
4. preflight or dry-run result;
5. dispatch authorisation;
6. command envelope;
7. command acknowledgement;
8. telemetry;
9. execution receipt;
10. mission verification;
11. accepted execution consequence, where separately promoted.

No stage automatically promotes to a later stage merely because it exists, is machine-generated, is syntactically valid, or was accepted by an external system. Each harder stage requires its own authority, evidence, freshness, safety, command-integrity, and promotion posture.

A `MissionPlan` is not a `CommandEnvelope`. A `CommandAcknowledgement` is not an accepted execution consequence. A `MissionExecutionReceipt` is evidence candidate material, not accepted execution truth by itself. A `MissionVerification` may support promotion only through ordinary OFARM review, evidence, current-state, and accepted-consequence law.

### CP12-C.4 Mission authority and human-governed defaults

CP12 adds mission-sensitive action classes that must be evaluated through ordinary OFARM authority law. A broad role, agent capability, model confidence, tool success, preflight success, CP11 charter pass, machine capability declaration, command acknowledgement, or vendor adapter result is not enough.

The following mission-sensitive actions are recognised for CP12 governance:

- `MISSION_PREPARE_CANDIDATE`;
- `MISSION_REQUEST_PREFLIGHT`;
- `MISSION_APPROVE_PLAN`;
- `MISSION_APPROVE_DISPATCH`;
- `MISSION_DISPATCH_COMMAND`;
- `MISSION_ACKNOWLEDGE_COMMAND`;
- `MISSION_ABORT`;
- `MISSION_EMERGENCY_STOP`;
- `MISSION_OVERRIDE_TAKEOVER`;
- `MISSION_REPORT_TELEMETRY`;
- `MISSION_REPORT_EXECUTION_RECEIPT`;
- `MISSION_VERIFY_RESULT`;
- `MISSION_ACCEPT_VERIFICATION`;
- `MISSION_RECORD_NEAR_MISS`;
- `MISSION_RECORD_PHYSICAL_SAFETY_INCIDENT`;
- `MISSION_RESOLVE_PHYSICAL_SAFETY_INCIDENT`;
- `MISSION_ACTIVATE_POLICY_PACK`.

By default:

- software agents may prepare mission candidates, request preflight, run advisory simulations, and prepare review packages within their authority envelope;
- software agents may not dispatch physical commands by default;
- mission dispatch is human-governed or human-approval-required unless later accepted law explicitly grants bounded policy authority for a specific low-risk mission class;
- emergency stop must remain available through local safety and authorised human paths regardless of agent, pack, or vendor state;
- telemetry reporting may be machine-reported, but telemetry is not accepted execution truth by itself;
- mission verification and accepted execution consequences remain governed by ordinary OFARM evidence, review, promotion, and current-state law.

### CP12-C.5 Preflight, current-state, and CP11 charter preconditions

A mission preflight or dry-run is a no-side-effect evaluation. It may produce findings, blockers, evidence needs, charter-gate results, geometry findings, capability findings, safety findings, or review requirements. It may not create mission dispatch authority, command authority, accepted execution truth, Compliance Twin fact, or current-state mutation by itself.

A mission dispatch path that materially relies on current-state materialisation is a high-consequence use. If required current-state materialisation is stale, invalid, unavailable, disputed, or insufficiently based for the mission class, the permitted outcomes are recompute, refuse, require review, require human approval, or emit another policy-declared blocked disposition.

Where a mission materially implicates CP11 sustainability constraints, objectives, evidence, claim, exception, or breach posture, applicable CP11 gates must be evaluated before dispatch. A CP11 charter pass is a precondition where applicable, not dispatch authority.

### CP12-C.6 Geofence, no-go-zone, geometry, and execution-window law

A dispatchable mission must have a declared `MissionScope`, `MissionGeometryBasis`, and applicable spatial constraints. For mission classes that move or actuate in physical space, this includes governed `GeoFence`, `NoGoZone`, route, buffer, exclusion, or partial-extent constraints as required by the active mission policy.

Geometry used for dispatch must be traceable to its basis and freshness posture. An external map, vendor route, imported geometry, or adapter payload is not mission truth by itself.

A dispatchable mission must also declare an `ExecutionWindow` with temporal coherence. Expired, not-yet-valid, ambiguous, stale, or conflicting execution windows must block dispatch, require review, or require human approval according to policy.

### CP12-C.7 Mission safety constraints and physical actor capability

A mission-sensitive path must evaluate applicable `MissionSafetyConstraint` and `PhysicalActorCapabilityProfile` before dispatch. Safety constraints may include human proximity, animal proximity, obstacle handling, slope/soil/terrain constraints, weather constraints, input/application constraints, equipment state, battery/fuel/energy state, communication state, local fallback state, emergency-stop availability, and override availability.

A physical actor capability declaration is descriptive, not dispositive. Vendor capability, machine telemetry, adapter mapping, or static manifest support is not safety proof and not dispatch authority by itself.

### CP12-C.8 Autonomy level, emergency stop, override, fallback, and remote takeover

CP12 recognises mission-specific autonomy posture. An autonomy level is not global actor identity and not general farm autonomy. It is a governed declaration for a mission class, physical actor, scope, execution window, authority context, supervision posture, fallback posture, and safety policy.

A dispatchable mission must declare applicable emergency-stop, human-override, local-fallback, lost-link, and remote-takeover posture. Absence, invalidity, or inapplicability of required safety posture must block dispatch, require review, or require human approval.

Emergency-stop and safety-critical fallback paths must not depend solely on cloud availability, LLM output, advisory-agent availability, or non-safety-rated public-operation success.

### CP12-C.9 Command envelope and command integrity

A `CommandEnvelope` is the governed package that may be sent to a physical actor or adapter for dispatch. It must identify the mission, command subject, command class, target actor, scope, execution window, authority basis, command integrity basis, expiry, replay-protection posture, and abort/override/fallback references required by policy.

A command must not be dispatched merely because a mission plan exists, a preflight passed, a CP11 charter evaluation passed, an agent tool call succeeded, or a vendor adapter accepted a payload.

Command acknowledgement confirms only that an external actor or adapter acknowledged a command envelope according to the declared external boundary. It is not accepted execution truth and not mission verification.

### CP12-C.10 Telemetry, execution receipt, verification, and accepted consequences

Mission telemetry and execution receipts are evidence candidates. They may support reconstruction, review, verification, incident handling, current-state materialisation, or accepted execution consequences only through ordinary OFARM evidence, review, authority, promotion, current-state, and twin-boundary law.

A `MissionVerification` records post-mission verification posture. Verification may compare expected mission scope, action, timing, safety constraints, telemetry, imagery, machine report, human observation, lab result, or other evidence. A completed mission is not a verified mission unless the mission-verification posture says so.

Accepted execution consequences must remain separate from machine-reported execution receipts and vendor logs.

### CP12-C.11 Incidents, aborts, near misses, and physical safety records

Mission aborts, emergency stops, fallback activations, remote takeovers, near misses, and physical safety incidents must be first-class records where applicable.

A `NearMissEvent` or `PhysicalSafetyIncident` does not automatically create a legal compliance fact, insurance fact, liability determination, or Compliance Twin fact unless a separate governed path creates that consequence. It must remain traceable and reviewable.

### CP12-C.12 External vendor and payload boundary

External machinery, robot, drone, actuator, sensor, irrigation, or tasking payloads may be mapped into OFARM only as external payloads, evidence candidates, command envelopes, telemetry envelopes, execution receipts, or adapter surfaces according to declared mapping coverage and loss posture.

External systems do not become hidden OFARM truth stores, hidden authority stores, hidden mission plans, hidden mission approvals, or hidden dispatch authorities by being integrated.

### CP12-C.13 Deferrals

CP12 does not define the full experimentation, causal-learning, farm-memory, seasonal-learning, or learning-promotion model. Those belong to CP13.

CP12 does not define full farm-to-farm intelligence, regional mission coordination, benchmark exchange, federated learning, derivative model-use, or shared fleet-coordination law. Those belong to CP14 or a later explicitly scoped amendment.

CP12 does not define generated-software delivery governance, robot adapter deployment, rollback, SBOM, build provenance, or generated workflow promotion. Those belong to CP15.

CP12 does not expand OFARM beyond the crop-only release boundary into livestock identity, welfare, feeding, treatment, movement, herd/flock, or animal-health semantics.

CP12 does not create legal safety certification, machinery certification, insurance readiness, product-liability determination, or production autonomous-operation readiness.

### CP12-C.14 Non-claims

CP12 does not claim production robot readiness, machine-control readiness, autonomous field-operation readiness, safety certification, legal advice, insurance advice, livestock mission readiness, external vendor protocol completeness, live robot integration, live machinery integration, fleet optimisation readiness, CP13 readiness, CP14 readiness, or CP15 readiness.
```

#### Reason

The Constitution needs a model-law boundary for cyber-physical missions. CP11 explicitly deferred robot/machine mission law to CP12. Without this patch, OFARM has strong truth, agent, charter, and intervention law, but not enough baseline law for the physical execution boundary.

#### Interaction with existing law

This patch preserves:

- assertion/history-first truth;
- current-state materialisation;
- Advisory/Compliance Twin separation;
- authority/default-deny law;
- pack law;
- query/output law;
- agent run/tool-manifest law;
- CP11 charter gates.

It uses existing concepts such as `InterventionIntentPayload`, `ExecutionRecordPayload`, `PartialExtent`, `MaterializationBasis`, `AuthorizationDecisionTrace`, `AgentRunTrace`, and `SustainabilityPolicyEvaluationTrace` by reference rather than replacing them.

#### Risk of contradiction

Medium. The main risk is accidentally making CP12 look like execution implementation, vendor protocol, or safety certification. The patch mitigates this by explicitly framing CP12 as mission-envelope law and by making telemetry/command acknowledgement non-authoritative by themselves.

#### Baseline law now or RFC law?

The invariant-level boundary belongs in baseline. Detailed lifecycle fields, schemas, event payloads, geometry objects, command integrity fields, and conformance cases belong in the CP12 RFC, machine contracts, and companion artifacts.

#### Migration note

Existing planned interventions, prescriptions, task cards, machine exports, vendor logs, telemetry streams, and execution records must not be reclassified as CP12 mission envelopes unless explicitly mapped. Existing material may be linked as source evidence or legacy/import material.

#### Conformance implication

CP12 conformance must prove that mission candidates, preflights, CP11 charter passes, tool successes, command acknowledgements, telemetry receipts, and execution receipts do not self-promote into dispatch authority or accepted execution truth.

---

### 1.2 Patch C12-C-2 — Add CP12 to first-class domain objects

#### Exact section to add or amend

Amend:

```text
### 7.24 First-class domain objects
```

#### Proposed normative text

Add a new bullet group:

```text
CP12 cyber-physical mission objects are first-class domain objects when present in an active profile or accepted RFC scope. These include `CyberPhysicalMissionEnvelope`, `MissionIntent`, `MissionCandidate`, `MissionPlan`, `MissionScope`, `MissionPreflightTrace`, `MissionDispatchAuthorization`, `CommandEnvelope`, `MissionTelemetryEnvelope`, `MissionExecutionReceipt`, `MissionVerification`, `MissionAbortEvent`, `NearMissEvent`, and `PhysicalSafetyIncident`.

They are not aliases for existing intervention intent or execution record objects. They may reference intervention intent and execution records, but they preserve the boundary between planned operation, physical mission authority, command dispatch, machine-reported execution, and accepted execution consequence.
```

#### Reason

CP12 mission objects must not be treated as comments, UI state, vendor payloads, or hidden runtime records.

#### Interaction with existing law

This extends the domain-object list without changing existing lifecycle or identity law.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline law for object recognition; RFC/machine-contract detail later.

#### Migration note

Legacy mission-like records must be migrated as candidate mission material or source evidence unless they satisfy CP12 identity and lifecycle requirements.

#### Conformance implication

Conformance must verify that mission objects are explicitly typed and not stored only in projections, adapters, or vendor logs.

---

### 1.3 Patch C12-C-3 — Add CP12 authority action classes

#### Exact section to add or amend

Insert after:

```text
### 7.10 AuthorityActionClass
```

or, if preserving CP11 addendum-only style, include within `### CP12-C.4 Mission authority and human-governed defaults` above.

#### Proposed normative text

```text
CP12 adds mission-sensitive `AuthorityActionClass` values:

- `MISSION_PREPARE_CANDIDATE`;
- `MISSION_REQUEST_PREFLIGHT`;
- `MISSION_APPROVE_PLAN`;
- `MISSION_APPROVE_DISPATCH`;
- `MISSION_DISPATCH_COMMAND`;
- `MISSION_ACKNOWLEDGE_COMMAND`;
- `MISSION_ABORT`;
- `MISSION_EMERGENCY_STOP`;
- `MISSION_OVERRIDE_TAKEOVER`;
- `MISSION_REPORT_TELEMETRY`;
- `MISSION_REPORT_EXECUTION_RECEIPT`;
- `MISSION_VERIFY_RESULT`;
- `MISSION_ACCEPT_VERIFICATION`;
- `MISSION_RECORD_NEAR_MISS`;
- `MISSION_RECORD_PHYSICAL_SAFETY_INCIDENT`;
- `MISSION_RESOLVE_PHYSICAL_SAFETY_INCIDENT`;
- `MISSION_ACTIVATE_POLICY_PACK`.

The default posture is deny unless an applicable authority path exists. Mission dispatch, emergency-stop override, remote takeover, accepted verification, and physical-safety incident resolution are high-governance action classes by default.
```

#### Reason

Physical action cannot be governed by generic roles or agent capabilities.

#### Interaction with existing law

This is an additive authority-action extension. It preserves default deny and human-governed defaults.

#### Risk of contradiction

Low if the Authority Action Matrix is extended in the RFC/addendum layer.

#### Baseline law now or RFC law?

Baseline can name action classes. Default posture matrix belongs in the CP12 RFC addendum to the Authority Action Matrix.

#### Migration note

Existing authority grants do not automatically grant CP12 mission-dispatch authority.

#### Conformance implication

Conformance must include fixtures where mission dispatch without authority trace fails, and where an agent cannot dispatch by tool success.

---

### 1.4 Patch C12-C-4 — Amend high-consequence use rule for mission dispatch

#### Exact section to add or amend

Insert after:

```text
### 10.15 High-consequence use rule
```

and after CP11 high-consequence addenda if physically located later.

#### Proposed normative text

```text
### CP12 high-consequence mission-dispatch reliance

Mission dispatch, command envelope creation, command dispatch, mission verification, and accepted mission-execution consequence are high-consequence uses.

Where such use materially relies on current-state materialisation, geometry, actor capability, safety posture, CP11 charter evaluation, authority status, pack/profile state, or external adapter mapping, the high-consequence freshness and basis rules apply.

If any required basis is stale, invalid, unavailable, disputed, insufficiently based, expired, or outside declared scope, the permitted outcomes are recompute, refuse, require review, require human approval, or emit another policy-declared blocked disposition. Silent dispatch is prohibited.
```

#### Reason

Physical dispatch has consequences beyond advisory output. It must inherit the strongest current-state and basis discipline.

#### Interaction with existing law

This extends the existing high-consequence rule; it does not rewrite current-state law.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline invariant now; exact fields and freshness classes in CP12 RFC/machine contracts.

#### Migration note

Existing machine-command exports must be treated as non-CP12 or blocked/qualified until they can prove freshness and basis.

#### Conformance implication

Add `mission_dispatch_with_stale_current_state_fails` and `mission_dispatch_with_expired_execution_window_fails`.

---

### 1.5 Patch C12-C-5 — Add CP12 to event grammar policy

#### Exact section to add or amend

Amend:

```text
## 13. Event grammar policy
```

and append a CP12-specific cross-reference after `### 13.4 Pack-level enrichment`.

#### Proposed normative text

```text
### 13.5 CP12 mission event discipline

CP12 mission events are semantic events subject to normal OFARM event, commit, promotion, and accepted-consequence law.

Mission-related event families include candidate preparation, preflight, dispatch authorization, command envelope creation, command acknowledgement, telemetry reporting, execution receipt reporting, verification, abort, emergency stop, fallback activation, remote takeover, near miss, and physical safety incident.

Receiving a mission event, telemetry record, command acknowledgement, or execution receipt is not acceptance of its consequence into current-state materialisation or Compliance Twin truth. Accepted consequences require the declared review, evidence, authority, promotion, and verification path.
```

#### Reason

Mission events must not be treated as transport logs or automatic truth.

#### Interaction with existing law

This reuses event grammar and accepted event consequence law.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline event discipline. Detailed event family table belongs in companion/RFC.

#### Migration note

Vendor telemetry events become source events or evidence candidates unless promoted.

#### Conformance implication

Add `telemetry_receipt_does_not_create_accepted_execution_truth` and `command_acknowledgement_does_not_create_execution_truth`.

---

### 1.6 Patch C12-C-6 — Add CP12 conformance baseline

#### Exact section to add or amend

Amend:

```text
### 15.1 Minimum constitutional conformance baseline
```

#### Proposed normative text

Add:

```text
For CP12 mission-sensitive use, a conforming implementation must demonstrate that:

- mission candidates and preflight results do not create mission dispatch authority;
- CP11 charter pass does not create mission dispatch authority;
- software-agent tool success does not create mission dispatch authority;
- dispatch requires a mission envelope, authority trace, safety envelope, command integrity posture, execution window, and required geofence/no-go-zone basis where applicable;
- dispatch fails or routes to review when required current-state, geometry, actor capability, charter, authority, or safety posture is stale, invalid, missing, expired, disputed, or insufficiently based;
- command acknowledgement, telemetry, and execution receipt do not create accepted execution truth by themselves;
- mission verification is distinct from mission execution receipt;
- near-miss and physical-safety incident records do not automatically create legal, insurance, or Compliance Twin facts;
- emergency-stop, human-override, local-fallback, and lost-link policies are represented for mission classes requiring them;
- CP12 does not create CP13, CP14, CP15, livestock, legal-certification, or production-autonomy claims.
```

#### Reason

Baseline law must define the minimum conformance target before schemas are drafted.

#### Interaction with existing law

Extends existing conformance posture.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline minimum; fixture suite later.

#### Migration note

No CP12 production-readiness claim until conformance fixtures exist and pass.

#### Conformance implication

Defines the minimum CP12 conformance fixture family for Phase 5/6.

---

### 1.7 Patch C12-C-7 — Add CP12 glossary entries

#### Exact section to add or amend

Append to:

```text
## 17. Glossary
```

or include in the CP12 baseline addendum until the next full glossary consolidation.

#### Proposed normative text

```text
### CyberPhysicalMissionEnvelope
A governed envelope binding mission identity, scope, stage, authority basis, safety basis, geometry basis, execution window, command integrity, actor capability, telemetry, verification, and output posture for a cyber-physical mission path.

### MissionIntent
A declared operational purpose or need for a possible physical mission. It is not a mission plan and not dispatch authority.

### MissionCandidate
A candidate mission constructed for evaluation, simulation, preflight, or review. It is not dispatch authority.

### MissionPlan
A reviewed or prepared plan for a physical mission. It is not a command envelope and not proof of execution.

### MissionDispatchAuthorization
A governed authorisation decision permitting a specific mission dispatch within scope, time, authority, safety, command-integrity, current-state, and charter limits.

### CommandEnvelope
A governed command package prepared for a physical actor or adapter. It is not accepted execution truth.

### MissionTelemetryEnvelope
A governed wrapper for mission telemetry. Telemetry is evidence candidate material, not accepted execution truth by itself.

### MissionExecutionReceipt
A record that a physical actor, machine, adapter, or operator reported execution or completion. It is evidence candidate material, not accepted execution truth by itself.

### MissionVerification
A governed post-mission verification record comparing mission intent, scope, expected action, telemetry, evidence, safety constraints, and outcome posture.

### GeoFence
A spatial boundary limiting where a mission may occur.

### NoGoZone
A spatial exclusion rule prohibiting mission movement or actuation in a declared area.

### MissionSafetyConstraint
A mission-specific safety constraint, threshold, prohibition, or required condition.

### PhysicalActorCapabilityProfile
A governed description of a physical actor's relevant capabilities and limits. It is descriptive, not safety proof or authority by itself.

### AutonomyLevelDeclaration
A mission-specific declaration of autonomy posture for a physical actor, scope, execution window, supervision state, fallback posture, and safety policy.

### EmergencyStopPolicy
A governed policy describing how a mission may be stopped in safety-critical or policy-blocked conditions.

### HumanOverridePolicy
A governed policy describing how authorised humans may intervene, override, take over, or abort a mission.

### LocalFallbackPolicy
A governed policy describing how a mission behaves when cloud, network, agent, or external-service dependency is unavailable.

### NearMissEvent
A governed record of a mission-related safety event that could have caused harm or violation but did not result in confirmed incident consequence by itself.

### PhysicalSafetyIncident
A governed record of a mission-related safety incident. It is not a legal, insurance, liability, or Compliance Twin fact unless separately promoted through active law.
```

#### Reason

CP12 introduces baseline-recognised concepts requiring consistent terminology.

#### Interaction with existing law

No conflict.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Glossary entries can be baseline; detailed fields remain RFC/machine contracts.

#### Migration note

Use these terms consistently in Phase 5 schemas.

#### Conformance implication

Schema names should match glossary terms.

---

## 2. File: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`

### 2.1 Patch C12-P-1 — Add CP12 mission gate to EnforcementChain

#### Exact section to add or amend

Amend:

```text
### 3.1 EnforcementChain
```

and insert after:

```text
### 3.5 Pack/profile applicability gate
```

or after the CP11 charter gate where physically appended.

#### Proposed normative text

Add to the gate list:

```text
- mission-envelope and cyber-physical safety gate where mission-sensitive use is present;
```

Add new section:

```text
### CP12-P.1 Mission-envelope and cyber-physical safety gate

For mission-sensitive use, the platform must resolve the applicable `CyberPhysicalMissionEnvelope` and mission stage before command creation, command dispatch, telemetry acceptance as evidence candidate, mission verification, or accepted execution consequence.

The gate must evaluate, as applicable:

- mission identity and lifecycle state;
- mission stage separation;
- mission authority action and `AuthorizationDecisionTrace`;
- mission preflight result;
- CP11 charter precondition result;
- current-state and materialisation freshness;
- mission geometry basis;
- geofence and no-go-zone constraints;
- execution window and temporal coherence;
- actor capability and compatibility;
- mission safety constraints;
- autonomy-level declaration;
- emergency-stop policy;
- human-override policy;
- local-fallback and lost-link policy;
- command envelope integrity;
- command expiry and replay-protection posture;
- external adapter mapping coverage and loss posture;
- mission output qualification.

The gate must produce or link to a mission preflight trace, dispatch-authorisation trace, command envelope, telemetry envelope, execution receipt, verification record, incident record, or blocked-action result according to the mission stage and outcome.

A pass through this gate is not by itself accepted execution truth. Accepted execution consequences require ordinary OFARM evidence, review, promotion, and current-state law.
```

#### Reason

Runtime needs an explicit cyber-physical gate. Otherwise mission safety is only RFC prose.

#### Interaction with existing law

Fits into existing enforcement architecture and CP11 charter gate. It does not replace authority, validation, evidence, review, current-state, or publication/export gates.

#### Risk of contradiction

Medium. Risk is treating a gate pass as execution truth. The text explicitly prevents this.

#### Baseline law now or RFC law?

Runtime gate belongs in baseline. Field-level schema belongs later.

#### Migration note

Existing runtime surfaces are unaffected unless mission-sensitive.

#### Conformance implication

Add `mission_candidate_without_preflight_fails`, `mission_dispatch_without_authority_trace_fails`, and `mission_dispatch_without_geofence_fails`.

---

### 2.2 Patch C12-P-2 — Add mission-sensitive high-consequence runtime rule

#### Exact section to add or amend

Insert after:

```text
### 4.7 High-consequence use rule
```

and after CP11 charter-sensitive runtime addenda if appended later.

#### Proposed normative text

```text
### CP12-P.2 Mission-sensitive current-state and basis reliance

For runtime purposes, mission dispatch, command-envelope creation, command dispatch, mission verification, accepted mission-execution consequence, and mission-related output publication are high-consequence uses.

If such use materially relies on current-state materialisation, geometry basis, pack/profile state, actor capability, safety posture, execution-window validity, CP11 charter result, authority state, or external adapter mapping, the platform must prove the relevant basis, recompute it, refuse the action, require review, require human approval, or emit another policy-declared blocked or qualified disposition.

The platform must not silently dispatch a mission or present a mission as verified when required basis is stale, invalid, missing, expired, disputed, insufficient, permission-limited, or outside declared scope.
```

#### Reason

Runtime must not let stale current state, geometry, or capability data drive physical dispatch.

#### Interaction with existing law

Specialises current-state/freshness rule for mission-sensitive use.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline runtime rule.

#### Migration note

Legacy machine exports must be clearly non-CP12 or basis-qualified.

#### Conformance implication

Add stale/expired/missing-basis dispatch failure fixtures.

---

### 2.3 Patch C12-P-3 — Add AI mission-preparation boundary

#### Exact section to add or amend

Insert after:

```text
### 8.4 AI enforcement path
```

or after CP11 agent-run integration addendum.

#### Proposed normative text

```text
### CP12-P.3 AI and agent mission-preparation boundary

AI-generated mission candidates, mission plans, mission simulations, route suggestions, geofence proposals, safety checks, or command-envelope drafts must enter the same enforcement architecture as other mission-sensitive inputs.

A software agent may:

- prepare a mission candidate;
- request mission preflight;
- run advisory mission simulations;
- identify required evidence or current-state gaps;
- prepare a review or dispatch package;
- emit a blocked-action trace;
- prepare command-envelope candidates for review.

A software agent may not by default:

- approve mission dispatch;
- dispatch a command;
- perform emergency-stop override or remote takeover;
- accept mission verification;
- accept execution consequences;
- resolve physical-safety incidents;
- treat tool success, vendor acknowledgement, or model confidence as physical mission success.

Any mission-sensitive AI result must carry sufficient result qualification to expose target twin, mission stage, authority posture, preflight posture, current-state freshness, CP11 charter posture, geometry basis, actor capability basis, safety posture, command-integrity posture, and blocked or review-required gates.
```

#### Reason

Agents will be useful mission planners but must not become physical governors.

#### Interaction with existing law

Extends CP3/CP4/CP5 agent law and CP11 agent boundary.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline runtime boundary. Agent-run field links later.

#### Migration note

Existing mission-generation AI tools become advisory/preparation only unless CP12 authority is added.

#### Conformance implication

Add `agent_cannot_dispatch_mission_by_tool_success`.

---

### 2.4 Patch C12-P-4 — Add Advisory Twin mission simulation boundary

#### Exact section to add or amend

Insert after:

```text
### 9.5 Bridge enforcement
```

or after CP11 sustainability bridge addendum if appended.

#### Proposed normative text

```text
### CP12-P.4 Mission simulation and Advisory Twin boundary

Mission simulations, route simulations, safety simulations, autonomy simulations, actor-capability simulations, and execution-window simulations belong to the Advisory Twin by default.

They may inform preflight, reveal blockers, request evidence, prepare mission candidates, compare alternatives, or support review.

They may not directly create mission dispatch authority, command envelopes, command dispatch, accepted execution truth, Compliance Twin facts, safety certification, or output claims.

A bridge from mission simulation toward mission dispatch, command creation, accepted verification, or Compliance Twin consequence must re-evaluate the material through applicable CP12 mission-envelope, authority, current-state, geometry, safety, command-integrity, CP11 charter, pack/profile, and output gates.
```

#### Reason

Mission simulation is valuable but cannot become physical action by confidence or plausibility.

#### Interaction with existing law

Preserves existing Advisory/Compliance boundary.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline runtime boundary.

#### Migration note

Existing scenario outputs remain Advisory unless bridged.

#### Conformance implication

Add `mission_simulation_does_not_authorise_dispatch`.

---

### 2.5 Patch C12-P-5 — Add command/telemetry/execution truth boundary

#### Exact section to add or amend

Insert after:

```text
## 12. Eventing, integration, and sync architecture
```

or after `### 12.7 Event-trace retention`.

#### Proposed normative text

```text
### CP12-P.5 Command, telemetry, and execution truth boundary

A runtime command envelope, command acknowledgement, telemetry envelope, execution receipt, vendor log, robot log, drone log, machinery payload, or adapter response is not canonical truth by itself.

Command dispatch means a governed command envelope was issued according to declared boundary conditions. It is not proof that the physical actor executed the command.

Command acknowledgement means an external actor or adapter acknowledged the command according to the declared mapping boundary. It is not proof that the command was executed or completed.

Telemetry and execution receipts are evidence candidates. They must preserve source, actor, device, adapter, time, scope, geometry, integrity, mapping coverage, and loss posture where relevant.

Mission verification and accepted execution consequences require ordinary OFARM evidence, authority, review, promotion, current-state, and output law.
```

#### Reason

Machine telemetry is one of the most dangerous hidden truth-store candidates.

#### Interaction with existing law

Applies assertion/history and event-ingress discipline to CP12 mission data.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline runtime rule.

#### Migration note

Existing vendor telemetry imports should be classified as evidence candidates or source truth records, not accepted execution truth.

#### Conformance implication

Add `telemetry_receipt_does_not_create_accepted_execution_truth` and `mission_verification_required_for_completed_status`.

---

### 2.6 Patch C12-P-6 — Add output semantics for mission reporting

#### Exact section to add or amend

Insert after:

```text
### 10.4 Output semantics
```

or after CP11 sustainability output gate if appended.

#### Proposed normative text

```text
### CP12-P.6 Mission output and reporting semantics

A PassportView, DocumentAssembly, report, dashboard, API response, mission summary, vendor-facing payload, partner-facing output, or safety report that describes mission state must disclose its mission-output posture.

A mission output must not hide:

- mission stage;
- dispatch-authorisation posture;
- command-envelope posture;
- command-acknowledgement posture;
- telemetry and receipt posture;
- verification posture;
- accepted-execution consequence posture;
- current-state freshness;
- geometry basis;
- CP11 charter posture where applicable;
- authority and approval posture;
- incident, abort, fallback, near-miss, or safety-status limitations;
- allowed and prohibited downstream uses.

A mission summary is not proof of execution merely because it is generated from telemetry, vendor logs, a command acknowledgement, or an AI summary.
```

#### Reason

Mission outputs are easy to overread as proof that work happened or was safe.

#### Interaction with existing law

Extends output taxonomy and result qualification.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline runtime rule; output schema later.

#### Migration note

Legacy mission reports should be labelled according to their source and verification posture.

#### Conformance implication

Add `mission_output_cannot_claim_verified_completion_without_verification`.

---

### 2.7 Patch C12-P-7 — Add CP12 runtime addendum

#### Exact section to add or amend

Append after the current CP11 runtime-enforcement addendum:

```text
## CP11 Sustainable Autonomous Farming Charter runtime-enforcement addendum — 2026-05-21
```

#### Proposed normative text

```text
## CP12 Cyber-Physical Mission Envelope runtime-enforcement addendum — 2026-05-28

Status: runtime baseline-law harmonisation candidate pending CP12 RFC acceptance and later machine-contract/conformance review.

CP12 adds a runtime gate for mission-sensitive use. It does not add production robot readiness, machine-control readiness, autonomous field-operation readiness, fleet optimisation, safety certification, legal advice, insurance advice, livestock mission readiness, or vendor-protocol completeness.

For mission-sensitive use, runtime implementations must be able to:

- resolve the active cyber-physical mission envelope and mission stage;
- distinguish mission intent, candidate, plan, preflight, dispatch authorisation, command envelope, acknowledgement, telemetry, execution receipt, verification, and accepted execution consequence;
- enforce mission authority action classes through ordinary authority/default-deny law;
- evaluate current-state freshness and materialisation basis for mission dispatch;
- evaluate CP11 charter preconditions where material;
- evaluate geometry basis, geofence, no-go-zone, route, and execution-window coherence;
- evaluate actor capability, safety constraints, autonomy posture, emergency-stop, human-override, local-fallback, lost-link, and remote-takeover posture;
- require command integrity, expiry, and replay-protection posture for dispatchable command envelopes;
- preserve telemetry and execution receipts as evidence candidates, not accepted execution truth by themselves;
- require mission verification before verified-completion or accepted-execution claims;
- represent abort, emergency-stop, fallback, remote-takeover, near-miss, and physical-safety incident records without automatically creating legal or Compliance Twin facts;
- qualify mission outputs according to mission stage, evidence, verification, authority, safety, and allowed/prohibited use.

CP12 runtime support remains implementation-directed with bounded debt until CP12 machine contracts, conformance fixtures, hostile review, and implementation evidence are present.
```

#### Reason

The runtime file needs a CP12 addendum matching the CP11 addendum style.

#### Interaction with existing law

Additive.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline runtime posture.

#### Migration note

Capability manifests must not claim CP12 runtime readiness until conformance and implementation evidence exist.

#### Conformance implication

Defines runtime conformance claims and non-claims.

---

## 3. File: `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

### 3.1 Patch C12-A-1 — Add CP12 concept rows

#### Exact section to add or amend

Append after:

```text
## CP11 Sustainable Autonomous Farming Charter alignment addendum — 2026-05-21
```

#### Proposed normative text

```text
## CP12 Cyber-Physical Mission Envelope alignment addendum — 2026-05-28

Status: alignment-register candidate for CP12 once `OFARM_Cyber_Physical_Mission_Envelope_RFC_v0_1.md` is accepted.

CP12 introduces the following baseline-recognised cyber-physical mission concepts. These concepts are not introduced by one vendor adapter, robot application, machinery payload, AI tool result, dashboard, output template, or external protocol.

| OFARM canonical concept | Main layer | Alignment class | Primary external semantic anchor(s) | Canonical naming choice | Reason for choice |
|---|---|---|---|---|---|
| CyberPhysicalMissionEnvelope | Governance / Cyber-physical mission | OFARM_OWNED | Tasking/OT/machinery standards as anchors only | OFARM uses `CyberPhysicalMissionEnvelope` | OFARM needs a governed envelope for mission identity, authority, safety, command integrity, telemetry, verification, and output posture. |
| MissionIntent | Planning / Mission | OFARM_OWNED | Planning foundations only | OFARM uses `MissionIntent` | OFARM needs to distinguish operational intent from mission plan and command authority. |
| MissionCandidate | Planning / Mission | OFARM_OWNED | None | OFARM uses `MissionCandidate` | OFARM needs a pre-authority candidate object for evaluation and review. |
| MissionPlan | Planning / Mission | OFARM_OWNED | None | OFARM uses `MissionPlan` | OFARM needs a plan object that is not a command envelope and not proof of execution. |
| MissionScope | Scope / Mission | OFARM_OWNED | GeoSPARQL/geometry anchors where applicable | OFARM uses `MissionScope` | OFARM needs explicit mission scope across farm, field, zone, crop, geometry, actor, and time. |
| MissionPreflightTrace | Runtime / Mission | OFARM_OWNED | Test/preflight foundations only | OFARM uses `MissionPreflightTrace` | OFARM needs no-side-effect mission preflight traces distinct from dispatch authority. |
| MissionDispatchAuthorization | Authority / Mission | OFARM_OWNED | Authority/action-class foundations only | OFARM uses `MissionDispatchAuthorization` | OFARM needs explicit authorisation for physical mission dispatch. |
| CommandEnvelope | Runtime / Command | OFARM_OWNED | External command/tasking protocols as mappings only | OFARM uses `CommandEnvelope` | OFARM needs a governed package for physical command dispatch without importing vendor payloads as truth. |
| CommandSignature | Runtime / Command integrity | OFARM_OWNED | Cryptographic/signature standards as implementation anchors | OFARM uses `CommandSignature` | OFARM needs command integrity, expiry, and replay-protection posture. |
| CommandAcknowledgement | Runtime / Command | OFARM_OWNED | Vendor acknowledgements as payload anchors only | OFARM uses `CommandAcknowledgement` | OFARM needs to separate acknowledgement from execution truth. |
| ExecutionWindow | Time / Mission | OFARM_ALIGNED | OWL-Time/profiled temporal foundations | OFARM uses `ExecutionWindow` | OFARM needs temporal validity and coherence for dispatch. |
| GeoFence | Spatial / Mission | OFARM_ALIGNED | GeoSPARQL / OGC anchors where applicable | OFARM uses `GeoFence` | OFARM needs dispatch-limiting spatial boundaries. |
| NoGoZone | Spatial / Mission | OFARM_ALIGNED | GeoSPARQL / OGC anchors where applicable | OFARM uses `NoGoZone` | OFARM needs explicit exclusion zones for mission safety and policy. |
| RouteConstraint | Spatial / Mission | OFARM_ALIGNED | GeoSPARQL / routing anchors where applicable | OFARM uses `RouteConstraint` | OFARM needs route/path constraints without making vendor routes hidden truth. |
| MissionGeometryBasis | Spatial / Evidence | OFARM_OWNED | GeoSPARQL/provenance anchors | OFARM uses `MissionGeometryBasis` | OFARM needs provenance and freshness of geometry used for dispatch. |
| MissionSafetyConstraint | Safety / Mission | OFARM_OWNED | OT/safety standards as external context only | OFARM uses `MissionSafetyConstraint` | OFARM needs mission-specific safety constraints independent of vendor capability claims. |
| PhysicalActorCapabilityProfile | Actor / Capability | OFARM_OWNED | Machinery/robot standards as profiles only | OFARM uses `PhysicalActorCapabilityProfile` | OFARM needs actor capability declarations that remain descriptive, not authority or safety proof. |
| RobotCapabilityProfile | Actor / Capability | OFARM_OWNED | Robot/vendor standards as profiles only | OFARM uses `RobotCapabilityProfile` | OFARM needs robot-specific capability posture without importing vendor law. |
| MachineCapabilityProfile | Actor / Capability | OFARM_OWNED | ISO 11783/ISOBUS and vendor payloads as profiles/mappings only | OFARM uses `MachineCapabilityProfile` | OFARM needs machine/implement capability posture without treating machinery declarations as dispatch authority. |
| AutonomyLevelDeclaration | Governance / Autonomy | OFARM_OWNED | Automation/safety taxonomies as external context only | OFARM uses `AutonomyLevelDeclaration` | OFARM needs mission-specific autonomy posture, not global actor autonomy. |
| EmergencyStopPolicy | Safety / Mission | OFARM_OWNED | Safety engineering anchors only | OFARM uses `EmergencyStopPolicy` | OFARM needs explicit emergency-stop posture for mission classes requiring it. |
| HumanOverridePolicy | Safety / Authority | OFARM_OWNED | Authority/safety anchors only | OFARM uses `HumanOverridePolicy` | OFARM needs explicit authorised human intervention and takeover paths. |
| LocalFallbackPolicy | Safety / Runtime | OFARM_OWNED | OT/offline resilience anchors only | OFARM uses `LocalFallbackPolicy` | OFARM needs mission behaviour when cloud, network, agent, or external services are unavailable. |
| LostLinkPolicy | Safety / Runtime | OFARM_OWNED | OT/offline resilience anchors only | OFARM uses `LostLinkPolicy` | OFARM needs mission behaviour when communications are lost. |
| RemoteTakeoverEvent | Event / Safety | OFARM_OWNED | None | OFARM uses `RemoteTakeoverEvent` | OFARM needs governed records for remote takeover without making takeover itself evidence of success. |
| MissionTelemetryEnvelope | Evidence / Runtime | OFARM_OWNED | SOSA/SSN, SensorThings, vendor telemetry as anchors/mappings only | OFARM uses `MissionTelemetryEnvelope` | OFARM needs telemetry as evidence candidate, not hidden execution truth. |
| MissionExecutionReceipt | Evidence / Runtime | OFARM_OWNED | Vendor/machinery receipts as payload anchors only | OFARM uses `MissionExecutionReceipt` | OFARM needs execution receipts distinct from accepted execution consequences. |
| MissionVerification | Evidence / Review | OFARM_OWNED | Provenance/verification foundations only | OFARM uses `MissionVerification` | OFARM needs verification posture before completed/verified/accepted claims. |
| MissionAbortEvent | Event / Mission | OFARM_OWNED | None | OFARM uses `MissionAbortEvent` | OFARM needs first-class abort records. |
| NearMissEvent | Safety / Event | OFARM_OWNED | Safety-reporting anchors only | OFARM uses `NearMissEvent` | OFARM needs near-miss safety records without automatic legal/compliance consequence. |
| PhysicalSafetyIncident | Safety / Event | OFARM_OWNED | Safety-reporting anchors only | OFARM uses `PhysicalSafetyIncident` | OFARM needs physical-safety incident records without automatic liability/compliance determination. |
| MissionOutputQualification | Output / Runtime | OFARM_OWNED | Result-qualification foundations only | OFARM uses `MissionOutputQualification` | OFARM needs mission outputs to disclose stage, authority, telemetry, verification, safety, and allowed/prohibited use. |

### CP12 alignment consequences

CP12 strengthens OFARM-owned governance around cyber-physical mission envelopes, but it does not create a robot runtime, vendor protocol, product-safety certification, legal certification, or autonomous farm-operation law.

External robotics, machinery, drone, IoT tasking, geospatial, safety, command, telemetry, or vendor standards may be admitted as anchors, profiles, mappings, runtime-surface contracts, or evidence sources. They do not become hidden OFARM law by being referenced.

Spatial and temporal concepts such as `GeoFence`, `NoGoZone`, `RouteConstraint`, and `ExecutionWindow` are intentionally `OFARM_ALIGNED` where the underlying geometry/time semantics should reuse existing standards. OFARM owns the governed mission carrier, boundary, authority, and consequence law, not every external spatial, machinery, or tasking protocol.

CP12 does not promote CP13 learning/farm-memory, CP14 farm-to-farm intelligence, CP15 generated-software delivery, livestock mission law, safety certification, or production autonomy readiness.
```

#### Reason

CP12 concepts must be explicitly visible in the Alignment Register before they are treated as constitutional core.

#### Interaction with existing law

This extends the register without changing CP11 or earlier concept alignment.

#### Risk of contradiction

Low if external standards remain anchors/profiles/mappings only.

#### Baseline law now or RFC law?

Alignment Register baseline update.

#### Migration note

Until this addendum is accepted, CP12 terms should remain candidate vocabulary.

#### Conformance implication

Phase 5 schemas should use these names and preserve the alignment classes.

---

## 4. File: `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

### 4.1 Patch C12-R-1 — Add CP12 readiness and claim-limit addendum

#### Exact section to add or amend

Append after:

```text
## CP11 Sustainable Autonomous Farming Charter readiness and claim-limit addendum — 2026-05-21
```

#### Proposed normative text

```text
## CP12 Cyber-Physical Mission Envelope readiness and claim-limit addendum — 2026-05-28

### Bounded continuation posture

CP12 improves the active baseline by adding a cyber-physical mission-envelope governance layer for mission-sensitive recommendation, planning, preflight, dispatch, command integrity, geofence/no-go-zone, safety posture, telemetry, execution receipt, verification, abort, near-miss, and physical-safety incident paths.

The CP12 layer is mission-envelope governance, not production robot automation, legal safety certification, vendor protocol completeness, or autonomous field-operation readiness.

CP12 should be treated as **implementation-directed with bounded debt** until the CP12 RFC, baseline patch, machine contracts, conformance fixtures, hostile review, implementation evidence, and real integration evidence are complete.

### Evidence currently available

CP12 currently provides or proposes:

- a Cyber-Physical Mission Envelope RFC draft;
- baseline patch text for Constitution, Platform Runtime, and Alignment Register;
- first-wave machine-contract candidates for mission envelope, command, safety, telemetry, verification, and incident objects;
- conformance fixture families;
- explicit deferrals to CP13, CP14, CP15, and future livestock/production-autonomy domains.

This is design and governance evidence. It is not live robot integration evidence, live machinery integration evidence, legal/safety certification evidence, insurance evidence, production runtime evidence, OT safety evidence, or live farmer-pilot evidence.

### Claims allowed after CP12 baseline acceptance

After CP12 is accepted and reconciled, the package may claim:

- bounded model-law support for cyber-physical mission-envelope governance;
- explicit stage separation between intent, candidate, plan, preflight, dispatch authorisation, command envelope, acknowledgement, telemetry, execution receipt, verification, and accepted consequence;
- explicit baseline hooks for geofence/no-go-zone, execution-window, command-integrity, emergency-stop, human-override, local-fallback, lost-link, telemetry, verification, abort, near-miss, and incident handling;
- controlled alignment of mission-sensitive paths with truth, authority, evidence, current-state, CP11 charter, pack, agent, Advisory/Compliance, query, and output law.

### Claims still blocked after CP12

The package must not claim:

- production robot readiness;
- production machine-control readiness;
- autonomous field-operation readiness;
- legal safety certification;
- insurance readiness;
- product-liability determination;
- live robot integration;
- live machinery integration;
- external vendor protocol completeness;
- fleet optimisation readiness;
- livestock mission readiness;
- CP13 learning/farm-memory readiness;
- CP14 farm-to-farm intelligence readiness;
- CP15 generated-software delivery readiness;
- safety of any physical actor, adapter, command, mission, or autonomy level beyond declared evidence and conformance scope.

### Evidence required before stronger CP12 claims

Stronger CP12 claims require:

- accepted CP12 machine contracts;
- passing CP12 conformance fixtures;
- runtime logs showing mission-envelope gate execution;
- authority traces for dispatch-sensitive actions;
- command-envelope integrity and replay-protection tests;
- geofence/no-go-zone and execution-window failure tests;
- emergency-stop, human-override, local-fallback, and lost-link evidence for relevant mission classes;
- telemetry and execution-receipt truth-boundary tests;
- verification and accepted-consequence promotion tests;
- incident and near-miss handling tests;
- live or simulated integration evidence for any external machinery, robot, drone, actuator, or tasking adapter claim;
- farmer/operator-facing comprehension and burden evidence for mission limitations, safety posture, and override/abort paths.
```

#### Reason

CP12 can easily be overclaimed as robot readiness. The readiness memo must block that.

#### Interaction with existing law

Continues CP10/CP11 readiness posture.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline readiness posture.

#### Migration note

No stronger CP12 claim without conformance and implementation evidence.

#### Conformance implication

Readiness claims must reference CP12 conformance results.

---

## 5. File: `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

### 5.1 Patch C12-H-1 — Add CP12 hostile-review update

#### Exact section to add or amend

Append after:

```text
## CP11 Sustainable Autonomous Farming Charter hostile-review addendum — 2026-05-21
```

#### Proposed normative text

```text
## CP12 Cyber-Physical Mission Envelope hostile-review addendum — 2026-05-28

A hostile reader should treat CP12 as a necessary cyber-physical mission-envelope extension, not as evidence that OFARM is now robot-ready, machine-control-ready, safety-certified, autonomous, or production-ready.

### Closed or substantially reduced by CP12

CP12 closes or reduces the following conceptual gaps:

- mission intent, candidate, plan, preflight, dispatch authorisation, command, acknowledgement, telemetry, execution receipt, verification, and accepted consequence are separated;
- recommendation, preflight pass, CP11 charter pass, tool success, capability declaration, command acknowledgement, telemetry, and execution receipt are not dispatch authority by themselves;
- mission dispatch requires explicit mission envelope, authority trace, safety envelope, command-integrity posture, and applicable current-state/charter gates;
- geofence, no-go-zone, route, geometry-basis, execution-window, and temporal-coherence concepts become baseline-recognised;
- emergency-stop, human-override, local-fallback, lost-link, and remote-takeover posture become baseline-recognised;
- mission telemetry and execution receipts become evidence candidates rather than hidden execution truth;
- mission verification is separated from machine-reported completion;
- aborts, emergency stops, fallback activations, remote takeovers, near misses, and physical-safety incidents become governed records;
- external vendor/machinery/robot/drone/tasking payloads are kept outside hidden OFARM truth, authority, and dispatch law;
- CP13, CP14, CP15, livestock mission law, legal safety certification, and production autonomy are explicitly deferred.

### Still open and hostile-reader relevant

CP12 does not close:

- production runtime evidence;
- live robot integration;
- live machinery integration;
- live drone/actuator/tasking integration;
- legal or safety certification;
- insurance or liability determination;
- fleet optimisation;
- vendor-specific protocol completeness;
- real-time safety controller implementation;
- hardware certification;
- farmer/operator UX validation;
- CP13 experimentation/farm-memory law;
- CP14 farm-to-farm intelligence law;
- CP15 generated-software delivery law;
- full CP12 conformance execution until fixtures and runners exist.

### Hostile-reader risks after CP12

The main post-CP12 risk is overclaiming mission-envelope law as physical-world safety readiness.

A hostile reader should reject any claim that CP12 makes a physical mission safe, legal, certified, insured, autonomous, vendor-compatible, or production-ready merely because the mission objects are represented.

The correct post-CP12 posture remains:

**implementation-directed with bounded debt, not production-ready, not autonomous, not safety-certified, not robot-ready, not vendor-protocol-complete, and not external-standard-ready.**
```

#### Reason

CP12 is high-risk for overclaiming. The hostile review must preserve claim discipline.

#### Interaction with existing law

Continues existing hostile-review pattern.

#### Risk of contradiction

Low.

#### Baseline law now or RFC law?

Baseline hostile-review posture.

#### Migration note

Use this as the hostile-review basis for CP12 Phase 6.

#### Conformance implication

Hostile review should require CP12 conformance execution before any stronger claims.

---

## 6. Summary table of patch decisions

| File | Patch | Baseline now? | Remain RFC/detail? | Risk |
|---|---:|---:|---:|---:|
| Constitution | CP12 mission-envelope boundary | Yes | Fields/schemas later | Medium |
| Constitution | CP12 core concepts | Yes | Detailed definitions later | Low |
| Constitution | Mission stage separation | Yes | Stage schemas later | Low |
| Constitution | Mission authority actions | Yes | Authority matrix addendum later | Low |
| Constitution | Preflight/current-state/CP11 preconditions | Yes | Contract details later | Low |
| Constitution | Geometry/execution-window/safety/capability law | Yes, invariant level | Details later | Medium |
| Constitution | Command/telemetry/verification truth boundary | Yes | Payload schemas later | Low |
| Constitution | CP12 event discipline | Yes, light | Event grammar table later | Low |
| Constitution | CP12 conformance baseline | Yes | Fixture suite later | Low |
| Platform Runtime | Mission-envelope gate | Yes | Trace schemas later | Medium |
| Platform Runtime | Mission-sensitive high-consequence rule | Yes | Use-class details later | Low |
| Platform Runtime | AI mission-preparation boundary | Yes | Agent-run linkage later | Low |
| Platform Runtime | Advisory mission simulation boundary | Yes | Scenario schemas later | Low |
| Platform Runtime | Command/telemetry truth boundary | Yes | Telemetry schemas later | Low |
| Platform Runtime | Mission output semantics | Yes | Output qualification schema later | Low |
| Alignment Register | CP12 concept rows | Yes | None | Low |
| Readiness Memo | CP12 claim limits | Yes | Evidence thresholds later | Low |
| Hostile Review | CP12 hostile-review update | Yes | Phase 6 will refine | Low |

---

## 7. Migration plan

Recommended migration order:

```text
1. Accept CP12 RFC draft as the working RFC candidate.
2. Apply Constitution patch C12-C-1 through C12-C-7 as candidate baseline text.
3. Apply Platform Runtime patch C12-P-1 through C12-P-7.
4. Apply Alignment Register patch C12-A-1.
5. Apply Readiness Memo patch C12-R-1.
6. Apply Hostile Review patch C12-H-1.
7. Proceed to CP12 Phase 5 machine-contract plan.
8. Proceed to CP12 Phase 6 hostile review.
9. Only then produce final CP12 repository package.
```

Do not merge CP12 as final baseline law until:

```text
- machine-contract implications are drafted;
- conformance fixture families are specified;
- hostile review has checked contradictions;
- safety/authority/current-state/CP11/agent/pack/output boundaries are hardened;
- final acceptance gate is passed.
```

---

## 8. Conformance implications to carry into Phase 5/6

The baseline patch creates the following mandatory CP12 conformance families:

```text
mission_candidate_without_preflight_fails
charter_pass_does_not_authorise_mission_dispatch
agent_cannot_dispatch_mission_by_tool_success
mission_dispatch_without_authority_trace_fails
mission_dispatch_without_mission_envelope_fails
mission_dispatch_without_geofence_fails
mission_dispatch_with_no_go_overlap_fails
mission_dispatch_with_expired_execution_window_fails
mission_dispatch_with_missing_emergency_stop_policy_fails
mission_dispatch_with_missing_human_override_policy_fails
mission_dispatch_with_missing_local_fallback_policy_fails
mission_dispatch_with_unsupported_physical_actor_capability_fails
mission_dispatch_with_stale_current_state_fails
mission_dispatch_with_failed_charter_gate_fails
command_without_signature_or_integrity_basis_fails
command_acknowledgement_does_not_create_execution_truth
telemetry_receipt_does_not_create_accepted_execution_truth
execution_receipt_does_not_create_verified_completion
mission_verification_required_for_completed_status
near_miss_record_does_not_auto_create_compliance_fact
physical_safety_incident_does_not_auto_create_liability_fact
valid_supervised_scouting_mission_passes
valid_human_approved_mechanical_weeding_mission_passes
valid_aborted_mission_with_emergency_stop_passes
```

---

## 9. Phase 4 conclusion

The CP12 baseline patch should proceed.

The patch is correctly bounded if it does only this:

```text
- makes the Cyber-Physical Mission Envelope visible in baseline law;
- adds CP12 concepts to the Alignment Register;
- adds mission-envelope runtime gate posture;
- separates intent/candidate/plan/preflight/dispatch/command/acknowledgement/telemetry/receipt/verification/accepted consequence;
- extends high-consequence/freshness/current-state/authority/output/agent/Advisory-Compliance boundaries to mission-sensitive use;
- updates readiness and hostile-review posture;
- preserves all existing OFARM truth, pack, authority, current-state, CP11 charter, Advisory/Compliance, and AI-agent safety law.
```

Recommended next command:

```text
Start CP12 Phase 5.

Create the CP12 machine-contract plan.

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
- relation to command integrity;
- relation to telemetry and verification;
- conformance tests;
- examples.

Then produce draft schema-style definitions in OFARM-compatible form.

Do not create full experimentation/farm-memory contracts except as forward references to CP13.
Do not create farm-to-farm intelligence contracts except as forward references to CP14.
Do not create generated-software delivery contracts except as forward references to CP15.
Do not claim robot/machine production readiness.
```


---

## Phase 7 reconciliation addendum

This final baseline patch candidate incorporates CP12 Phase 6 hostile-review findings and CP12 Phase 6.1 remediation.

The baseline patch should be read with the following additional constraints:

1. **Preflight pass is not dispatch authority.** A preflight pass is a gate result, not an authority grant, command envelope, execution receipt, or accepted consequence.
2. **A blocking failed preflight or safety result cannot support dispatch.** Runtime implementations must refuse, require review, or require human approval where blocking mission checks fail or are insufficient.
3. **Dispatch authorisation must be action-specific.** It may authorise mission dispatch or dispatch command only; it may not silently authorise verification, telemetry acceptance, incident resolution, learning, farm-to-farm exchange, or generated-software deployment.
4. **Command integrity is mandatory for dispatch-bound command envelopes.** Recipient binding, mission binding, dispatch-authorisation binding, payload digest, expiry, and replay protection are part of the CP12 command-integrity gate.
5. **Temporal coherence is a runtime mission gate.** Execution windows, dispatch validity, command validity, command integrity, and command acknowledgement must be coherent; expired or inverted windows cannot support dispatch or accepted acknowledgement.
6. **Capability compatibility must be fresh.** Dispatch-bound missions require verified and fresh compatibility with physical-actor capability, safety controls, command channel, mission scope, and execution-window posture.
7. **Emergency stop, human override, local fallback, lost-link, and remote takeover are not optional display fields where the mission class or autonomy level requires them.** They are safety-envelope preconditions.
8. **Mission telemetry, command acknowledgement, execution receipt, and vendor payloads are evidence candidates only.** They do not become accepted execution truth except through ordinary OFARM evidence, review, promotion, and current-state law.
9. **Mission outputs are qualified surfaces.** They may not silently become dispatch authority, execution truth, filed submission, attestation, or compliance fact.
10. **CP12 machine contracts remain draft/non-default.** No runtime or product should claim CP12 current/default contract support until a separate currentness-promotion decision is made.
