# OFARM Cyber-Physical Mission Envelope RFC v0.1

Date: 2026-05-28  
Status: final CP12 RFC candidate; accepted/merged; active below baseline authority into the active baseline  
Target path: `02_accepted_rfcs/OFARM_Cyber_Physical_Mission_Envelope_RFC_v0_1.md`  
Authority tier if accepted: accepted RFC; subordinate to `00_active_baseline/` and above companion artifacts under `PROJECT_AUTHORITY.md`  
Scope: introduce a bounded cyber-physical mission-envelope contract layer for mission identity, lifecycle, preflight, dispatch authority, geofence/no-go-zone discipline, command integrity, emergency stop, human override, local fallback, telemetry, execution receipt, verification, safety incident handling, output qualification, machine-contract implications, and conformance implications without reopening OFARM truth, current-state, pack, authority, output, CP11, or agent law.

---

## 1. Purpose

OFARM already has a strong semantic and governance spine:

- assertion/history-first canonical truth;
- governed current-state materialisation;
- one semantic substrate with Compliance Twin and Advisory Twin partitions;
- explicit authority, delegation, sharing, revocation, and default-deny posture;
- pack/profile law;
- query/output qualification and high-consequence output gates;
- sponsor-bound software-agent actorship;
- bounded agent run, trace, blocked-action, tool-manifest, and handoff law;
- advisory world-model boundaries;
- CP11 Sustainable Autonomous Farming Charter governance for sustainability-sensitive constraints, objectives, evidence, claims, exceptions, breaches, and output qualification.

That foundation is necessary but not sufficient for cyber-physical farming operations. A future OFARM runtime may prepare missions for robots, drones, tractors, implements, actuators, irrigation equipment, scouting devices, or other physical actors. Without explicit mission-envelope law, the platform can fail at the most dangerous boundary:

```text
recommendation / plan / CP11 charter pass / preflight pass / agent tool success / vendor payload
→ silently treated as dispatch authority
→ physical actor moves or actuates
```

This RFC introduces the first CP12 contract layer for a **Cyber-Physical Mission Envelope**.

The core decision is:

```text
Physical mission authority is not produced by recommendation, plan, preflight success, CP11 charter pass, agent confidence, tool invocation success, machine capability declaration, telemetry receipt, command acknowledgement, or adapter output alone.

Mission dispatch requires an explicit CP12 mission envelope, authority trace, safety envelope, command integrity, and applicable preflight/current-state/charter gates.

Telemetry and execution receipts are evidence candidates, not accepted execution truth by themselves.

Mission completion is not verified outcome unless verification and promotion posture are explicit.
```

CP12 is mission-envelope law. It is not a robotics product specification, not a vendor protocol, not full autonomy law, and not legal or safety certification.

---

## 2. Scope

This RFC covers cyber-physical mission governance for crop-farming OFARM contexts already within the active baseline scope.

It defines:

- CP12 authority, scope, and non-goals;
- `CyberPhysicalMissionEnvelope`;
- mission lifecycle;
- mission stage separation;
- mission authority actions;
- `MissionIntent`;
- `MissionCandidate`;
- `MissionPlan`;
- `MissionScope`;
- mission preflight and no-side-effect dry-run boundary;
- current-state freshness for dispatch;
- CP11 charter precondition interaction;
- geofence, no-go-zone, route, and geometry-basis law;
- execution-window and temporal-coherence law;
- `MissionSafetyConstraint`;
- physical actor capability and compatibility;
- mission-specific autonomy levels;
- emergency stop, human override, local fallback, lost-link fallback, and remote takeover posture;
- `CommandEnvelope`, command signature, command expiry, and replay-protection posture;
- `MissionDispatchAuthorization`;
- agent mission-preparation boundary;
- Advisory Twin mission simulation boundary;
- mission telemetry and execution receipt truth boundary;
- mission verification and accepted execution consequences;
- abort, emergency-stop, fallback, near-miss, and physical-safety incident records;
- external vendor/machinery/robot/drone/tasking payload boundaries;
- mission output qualification;
- mission event grammar and commit-matrix implications;
- mission pack/profile surface implications;
- data sovereignty for mission telemetry and safety records;
- machine-contract implications;
- conformance implications;
- readiness and non-claims;
- explicit deferrals to CP13, CP14, CP15, and future domains.

This RFC applies to **mission-sensitive uses**, including:

- preparation of a physical mission candidate;
- preflight or dry-run of a physical mission;
- approval of mission dispatch;
- creation of a command envelope;
- command dispatch or command acknowledgement;
- mission telemetry ingestion;
- execution receipt ingestion;
- mission verification;
- mission output/report generation;
- abort, emergency-stop, fallback, remote-takeover, near-miss, or physical-safety incident handling;
- adapter mapping from or to an external machinery/robot/drone/tasking payload;
- mission-related current-state or Compliance Twin reliance;
- mission-related AI-agent action;
- activation of packs or profiles that materially alter mission safety, autonomy, command integrity, geofence, verification, or external adapter posture.

---

## 3. Non-goals

This RFC does **not**:

1. Rewrite the OFARM Constitution.
2. Reopen assertion/history-first canonical truth.
3. Reopen governed current-state materialisation.
4. Reopen the Compliance Twin / Advisory Twin split.
5. Reopen pack merge law except for mission-specific surface-family additions or mappings.
6. Reopen core authority law except for mission-specific action-class additions or mappings.
7. Reopen CP11 Sustainable Autonomous Farming Charter law.
8. Create autonomous compliance decisioning.
9. Create full autonomous farm operation.
10. Create full fleet optimisation law.
11. Create a robotics product specification.
12. Create a vendor-specific robot, drone, implement, OEM API, ISOBUS, ISOXML, ADAPT, SensorThings, or tasking protocol specification.
13. Create legal, machinery-safety, insurance, or certification readiness.
14. Certify that any robot, machine, drone, implement, actuator, or vendor service is safe, compliant, insurable, or operationally ready.
15. Define full experimentation, farm-memory, causal-learning, or seasonal-learning law.
16. Define farm-to-farm intelligence, federated learning, regional mission coordination, shared hazard-map exchange, benchmark exchange, or regional-alert law.
17. Define generated-software deployment, robot-driver generation, adapter-generation, rollback, SBOM, or software-supply-chain law.
18. Expand OFARM from crop-farming operational law into livestock-specific identity, animal welfare, herd/flock, feeding, treatment, or animal-health mission law.
19. Treat external machine, robot, drone, OEM, or tasking standards as hidden OFARM mission law.
20. Treat mission preflight, CP11 charter pass, tool success, command acknowledgement, telemetry receipt, or execution receipt as accepted execution truth.

The full learning, experimentation, causal-evidence, and farm-memory model belongs to **CP13**.  
The full farm-to-farm intelligence and federated exchange boundary belongs to **CP14**.  
The full agentic software delivery, generated robot adapter, deployment, rollback, SBOM, and software-supply-chain governance layer belongs to **CP15**.

---

## 4. Authority relationship to the Constitution

If this RFC is accepted, it extends the active Constitution by introducing a cyber-physical mission-envelope layer.

The Constitution remains higher authority. This RFC must be interpreted under existing constitutional invariants:

- canonical truth is assertion/history-first;
- current state is governed materialisation, not hidden truth;
- Advisory Twin and Compliance Twin remain logical partitions over one semantic substrate;
- events do not change current state merely by existing;
- promotion requires declared safe paths;
- packs cannot mutate core meaning by stealth;
- external payloads are not hidden OFARM law;
- AI outputs, agent memory, tool success, manifests, vendor callbacks, telemetry, and generated summaries are not hidden truth stores or hidden governance decisions;
- authority is action-class-specific and default-deny;
- high-consequence use requires evidence, freshness, authority, and output qualification;
- CP11 charter-sensitive use remains subject to CP11 where material.

CP12 adds one constitutional invariant:

```text
No physical mission may be dispatched through OFARM merely because an intention, recommendation, plan, preflight result, CP11 charter pass, agent run, tool invocation, capability declaration, vendor payload, or command candidate exists.
```

Mission dispatch requires CP12 mission-envelope law and an explicit `MissionDispatchAuthorization` or later equivalent accepted machine contract.

---

## 5. Authority relationship to Platform Runtime

The Platform Runtime must realise CP12 through deterministic enforcement points.

For mission-sensitive use, the runtime must be able to:

- resolve mission identity and lifecycle state;
- distinguish mission intent, candidate, plan, preflight, dispatch authorisation, command envelope, telemetry, execution receipt, verification, and accepted consequences;
- evaluate authority for mission-specific action classes;
- enforce mission preflight where required;
- enforce current-state freshness for dispatch where current state is material;
- link CP11 charter evaluation where mission execution materially affects CP11 constraints, objectives, trade-offs, exceptions, breaches, or claims;
- evaluate geofence, no-go-zone, route, and geometry-basis posture;
- enforce execution-window and command-expiry constraints;
- evaluate mission safety constraints;
- evaluate physical actor capability compatibility;
- evaluate autonomy-level eligibility;
- require emergency-stop, human-override, and local-fallback posture for dispatchable mission classes;
- require command integrity, recipient binding, expiry, and replay protection for command envelopes;
- preserve telemetry and execution receipt as evidence candidates unless promoted by existing evidence/review/promotion law;
- require mission verification before treating mission completion as verified outcome;
- preserve mission event and incident traces;
- qualify mission-sensitive outputs;
- preserve data sovereignty for mission telemetry, incident, and verification records.

The runtime may optimise service topology, storage, adapters, UI, caches, command staging, or telemetry ingestion. It may not optimise by flattening CP12 stages, treating telemetry as truth, treating preflight as authorisation, treating command acknowledgement as execution, or treating mission verification as Compliance Twin fact without promotion.

---

## 6. Definitions

| Term | Meaning |
|---|---|
| CyberPhysicalMissionEnvelope | Governed mission container linking intent, candidate/plan, scope, actor, preflight, authority, command, safety, telemetry, receipt, verification, and incident traces. It is not itself dispatch authority or execution truth. |
| Physical actor | A robot, drone, tractor, machine, implement, actuator, irrigation controller, sensor-actuator device, or other device/service capable of physical-world movement, treatment, actuation, sensing-as-tasking, or operational effect. |
| Mission intent | Desired physical objective or task. It is not command, authorisation, execution, or verification. |
| Mission candidate | Candidate mission package prepared for preflight, review, comparison, or approval. It is not approved or dispatched. |
| Mission plan | Structured plan with scope, actor, route/area, timing, constraints, safety posture, and expected outputs. It is not dispatch by itself. |
| Mission scope | The spatial, temporal, operational, actor, autonomy, safety, and policy scope within which a mission may be considered. |
| Mission preflight | A no-authoritative-side-effect check of mission readiness, including authority, current-state freshness, CP11 charter posture where material, geometry, safety, physical actor compatibility, autonomy, fallback, and command-readiness gates. |
| Mission dispatch authorisation | A governed decision allowing command dispatch for a mission within declared scope and time. It is not execution truth. |
| Command envelope | Dispatchable command package bound to mission, recipient, scope, expiry, integrity basis, and authorisation posture. It is not proof of execution. |
| Command signature | Integrity/authenticity basis for a command envelope. It is not proof that the command was executed. |
| Geofence | Allowed physical operating area or boundary for a mission. |
| No-go zone | Prohibited, sensitive, buffered, unsafe, protected, or otherwise excluded area for a mission. |
| Mission safety constraint | Physical-safety rule for a mission, actor, environment, supervision, fallback, override, or execution context. |
| Physical actor capability profile | Capability declaration for robot/machine/drone/implement/actuator/sensor service. It is descriptive, not authority or safety proof. |
| Autonomy level declaration | Mission-specific autonomy posture, scoped by actor, mission class, conditions, authority, evidence, and revocation/downgrade rules. It is not global farm autonomy. |
| Emergency stop policy | Required stop/safe-state posture and authority path for mission classes where physical risk is material. |
| Human override policy | Required human intervention, supervision, override, takeover, or approval posture for mission classes where physical risk is material. |
| Local fallback policy | Required local safe-state behaviour when connectivity, control, sensor, power, actor, or command integrity fails. |
| Remote takeover event | Governed event recording transfer of live control or supervisory override. |
| Mission telemetry envelope | Runtime telemetry reported by a physical actor, adapter, sensor, or operator. It is evidence candidate only. |
| Mission execution receipt | Claimed mission execution or completion report. It is not verified outcome. |
| Mission verification | Post-mission verification record comparing mission plan, receipt, telemetry, observations, evidence, and actual outcome. It may support accepted consequences only through ordinary evidence/review/promotion law. |
| Near miss | Governed safety event where harm or prohibited physical interaction nearly occurred. It is not automatically legal or compliance fact. |
| Physical safety incident | Governed safety event involving actual harm, unsafe condition, uncontrolled action, protected-zone violation, emergency stop, or other physical safety concern. It is not automatically legal or compliance fact. |

---

## 7. Cyber-Physical Mission Envelope

`CyberPhysicalMissionEnvelope` is the top-level CP12 mission-governance container.

It may link:

```text
MissionIntent
MissionCandidate
MissionPlan
MissionScope
MissionPreflightTrace
MissionDispatchAuthorization
CommandEnvelope
CommandSignature
MissionTelemetryEnvelope
MissionExecutionReceipt
MissionVerification
MissionAbortEvent
EmergencyStopActivation
LocalFallbackActivation
RemoteTakeoverEvent
NearMissEvent
PhysicalSafetyIncident
MissionOutputQualification
```

A `CyberPhysicalMissionEnvelope` must declare:

- mission identity;
- mission stage/lifecycle state;
- mission class;
- target physical actor or actor class;
- mission scope;
- relevant farm/field/crop/zone/context references;
- authority posture;
- preflight posture;
- safety posture;
- CP11 charter posture where material;
- command posture where dispatch is contemplated;
- telemetry/receipt/verification posture where execution has been reported;
- incident/abort/fallback posture where applicable;
- prohibited interpretations.

A `CyberPhysicalMissionEnvelope` must carry or imply the following non-bypass clauses:

```text
NO_TRUTH_BYPASS
NO_AUTHORITY_BYPASS
NO_PREFLIGHT_AS_AUTHORIZATION
NO_CHARTER_PASS_AS_DISPATCH
NO_AGENT_TOOL_SUCCESS_AS_DISPATCH
NO_CAPABILITY_DECLARATION_AS_AUTHORITY
NO_VENDOR_PAYLOAD_AS_OFARM_LAW
NO_COMMAND_ACK_AS_EXECUTION_TRUTH
NO_TELEMETRY_AS_ACCEPTED_TRUTH
NO_RECEIPT_AS_VERIFICATION
NO_VERIFICATION_AS_COMPLIANCE_FACT_WITHOUT_PROMOTION
NO_AUTONOMY_SELF_UPGRADE
```

The mission envelope is the governed wrapper. It does not itself prove that the mission is authorised, dispatched, executed, verified, or accepted into current-state consequences.

---

## 8. Mission lifecycle

CP12 recognises a mission lifecycle distinct from truth and promotion state.

Recommended lifecycle states:

```text
CANDIDATE
PREFLIGHT_REQUESTED
PREFLIGHT_FAILED
PREFLIGHT_PASSED
AWAITING_APPROVAL
APPROVED_FOR_DISPATCH
DISPATCHED
IN_PROGRESS
PAUSED
ABORT_REQUESTED
ABORTED
COMPLETED_REPORTED
VERIFICATION_REQUIRED
VERIFICATION_RECORDED
VERIFIED
REJECTED_VERIFICATION
SUPERSEDED
CANCELLED
INCIDENT_REVIEW_REQUIRED
```

Lifecycle state must not be interpreted as accepted execution truth by label alone.

Rules:

1. `PREFLIGHT_PASSED` is not dispatch authorisation.
2. `APPROVED_FOR_DISPATCH` is not execution.
3. `DISPATCHED` is not execution.
4. `IN_PROGRESS` is not successful completion.
5. `COMPLETED_REPORTED` is not verified completion.
6. `VERIFICATION_RECORDED` is not accepted execution consequence unless promoted.
7. `VERIFIED` may support accepted execution consequences only through ordinary evidence, review, promotion, and materialisation law.
8. `INCIDENT_REVIEW_REQUIRED` may trigger review, evidence needs, authority restriction, or autonomy downgrade but is not automatically a legal or certification compliance fact.

Mission lifecycle state may be materialised for runtime coordination, but the mission lifecycle materialisation must remain derived and freshness-qualified under current-state law.

---

## 9. Mission stage separation

CP12 requires explicit separation between mission stages.

| Object | Meaning | Explicitly not |
|---|---|---|
| `MissionIntent` | Desired physical objective or task | Approval, command, dispatch, execution truth |
| `MissionCandidate` | Candidate package for preflight/review | Approved mission, command, execution truth |
| `MissionPlan` | Structured mission plan | Dispatched command, proof of execution |
| `MissionPreflightTrace` | No-side-effect readiness check | Dispatch authority, accepted truth |
| `MissionDispatchAuthorization` | Permission to dispatch within declared scope/time | Execution truth, verification |
| `CommandEnvelope` | Dispatchable command package | Execution proof, verification, accepted truth |
| `CommandAcknowledgement` | Recipient/channel acknowledgement | Execution proof, verification |
| `MissionTelemetryEnvelope` | Reported runtime data | Accepted truth, verification by itself |
| `MissionExecutionReceipt` | Claimed execution/completion report | Verified outcome |
| `MissionVerification` | Post-mission verification record | Compliance fact unless promoted |
| `NearMissEvent` / `PhysicalSafetyIncident` | Governed safety records | Automatic legal/compliance fact |

A conforming implementation must preserve these stage distinctions in data models, runtime gates, trace retrieval, user-facing outputs, and agent-facing surfaces.

---

## 10. Mission authority actions

CP12 extends authority action classification with mission-sensitive actions.

Mission action classes:

```text
MISSION_PREPARE_CANDIDATE
MISSION_REQUEST_PREFLIGHT
MISSION_APPROVE_DISPATCH
MISSION_DISPATCH_COMMAND
MISSION_ABORT
MISSION_EMERGENCY_STOP
MISSION_OVERRIDE_TAKEOVER
MISSION_REPORT_TELEMETRY
MISSION_REPORT_EXECUTION_RECEIPT
MISSION_VERIFY_RESULT
MISSION_ACCEPT_VERIFICATION
MISSION_RECORD_NEAR_MISS
MISSION_RECORD_PHYSICAL_SAFETY_INCIDENT
MISSION_RESOLVE_PHYSICAL_SAFETY_INCIDENT
MISSION_SET_AUTONOMY_LEVEL
MISSION_ACTIVATE_SAFETY_POLICY
MISSION_ACTIVATE_MISSION_POLICY_PACK
MISSION_SIGN_COMMAND_ENVELOPE
MISSION_REVOKE_DISPATCH_AUTHORIZATION
```

Default posture:

- software agents may prepare mission candidates when authorised;
- software agents may request preflight when authorised;
- software agents may assemble review packages, compare alternatives, explain blocked gates, and request evidence;
- software agents may not by default approve dispatch, sign commands, dispatch commands, disable emergency stop, disable human override, self-upgrade autonomy, accept mission verification, or resolve physical safety incidents;
- mission dispatch is default-deny unless an explicit `MissionDispatchAuthorization` resolves authority, scope, time, actor, safety, preflight, and command posture;
- emergency stop must remain available through authorised human/local safety paths and must not depend solely on ordinary agent-tool authority;
- remote takeover and override are safety-governed actions, not ordinary operational commands.

`MISSION_EMERGENCY_STOP` should not be blocked by ordinary workflow unavailability. It may still require identity/authority handling appropriate to safety-critical local control, but CP12 implementations must not make emergency stop depend on the same long-latency path as normal dispatch.

---

## 11. Mission preflight and no-side-effect dry-run boundary

`MissionPreflightTrace` is the CP12 readiness trace for mission dispatch.

A mission preflight may check:

- mission envelope completeness;
- mission lifecycle state;
- authority posture;
- current-state freshness;
- CP11 charter evaluation where material;
- geofence/no-go-zone geometry;
- route/extent/coverage posture;
- mission safety constraints;
- physical actor capability compatibility;
- autonomy-level eligibility;
- emergency stop posture;
- human override posture;
- local fallback posture;
- command integrity readiness;
- execution-window/temporal coherence;
- external adapter mapping coverage/loss where vendor payloads are used;
- telemetry and verification requirements;
- data-sovereignty or disclosure posture where material.

Mission preflight is necessary where declared by mission class or policy, but it is never sufficient for dispatch.

A mission preflight or dry-run must not:

- create accepted assertions;
- change current-state materialisations;
- activate packs;
- publish frozen outputs;
- promote evidence sufficiency;
- resolve identity permanently;
- consume inventory;
- create compliance facts;
- create execution truth;
- create mission dispatch authority;
- sign a command envelope;
- dispatch a command;
- create verified mission outcome.

A mission preflight may create diagnostic trace records clearly marked as preflight/dry-run trace.

Required preflight dispositions:

```text
PASS_CANDIDATE_ONLY
PASS_REQUIRES_DISPATCH_AUTHORIZATION
PASS_WITH_WARNINGS_REQUIRES_REVIEW
HUMAN_APPROVAL_REQUIRED
REVIEW_REQUIRED
BLOCKED
INSUFFICIENT_BASIS
STALE_STATE_RECOMPUTE_REQUIRED
CHARTER_GATE_FAILED
SAFETY_GATE_FAILED
GEOMETRY_GATE_FAILED
CAPABILITY_GATE_FAILED
COMMAND_INTEGRITY_GATE_FAILED
```

---

## 12. Current-state freshness for mission dispatch

A dispatchable mission that materially relies on current-state materialisation must prove current-state freshness for the relevant mission class.

Mission-critical current-state classes may include:

```text
geometry and boundary state
field / zone / crop-cycle state
crop stage where mission-relevant
soil / bearing / compaction / wetness state where mission-relevant
weather / wind / rain / visibility / temperature state where mission-relevant
water restriction or irrigation permission state
CP11 charter applicability and evaluation context
physical actor health and capability state
implement or actuator compatibility state
sensor trust state
known obstacle / sensitive-zone state
operator / supervisor availability state
authority / revocation / approval state
pack/profile activation state
```

If required current-state materialisation is stale, invalid, insufficient, disputed, or missing, the mission dispatch path must route to one of:

```text
REFUSE
RECOMPUTE_CURRENT_STATE
REQUIRE_REVIEW
REQUIRE_HUMAN_APPROVAL
STALE_STATE_SAFE_MODE
INSUFFICIENT_BASIS
```

A stale materialisation may be acceptable for exploratory advisory mission comparison, but not for dispatch, command signing, execution-bound preparation, or high-consequence mission output unless the relevant use policy explicitly allows a qualified disposition.

---

## 13. CP11 charter precondition interaction

Where mission execution materially affects sustainability constraints, objectives, trade-offs, exceptions, breaches, claims, or charter-sensitive output posture, CP12 must link the mission path to applicable CP11 evaluation.

A mission envelope may reference:

```text
SustainabilityPolicyEvaluationTrace
SustainabilityConstraint
SustainabilityObjective
TradeoffPolicy
SustainabilityEvidenceRequirement
SustainabilityOutputQualification
SustainabilityClaimBasis
CharterException
CharterBreach
```

Core rule:

```text
CP11 charter pass may satisfy one mission gate. It is not mission dispatch authority, command integrity, safety proof, execution proof, telemetry verification, or accepted current-state consequence.
```

If a mission requires a CP11 trace and the trace is missing, stale, incomplete, failed, blocked, or incompatible with mission scope/time, dispatch must refuse, recompute, require review, or require human approval according to policy.

A CP11 `CharterException` does not substitute for CP12 physical-safety exception, emergency-stop policy, geofence exception, command-integrity gate, or dispatch authorisation.

---

## 14. Geofence, no-go-zone, route, and geometry-basis law

CP12 defines mission geometry objects:

```text
GeoFence
NoGoZone
RouteCorridor
AllowedOperatingArea
ProhibitedOperatingArea
SensitiveZone
BoundaryBuffer
MissionExtent
PartialExecutionExtent
GeometryBasisRef
GeometryFreshnessState
GeometryConflictState
```

Mission classes involving movement, treatment, actuation, or spatially bounded operation must declare allowed operating area and known prohibited/sensitive areas unless a mission class profile explicitly states why geometry is not applicable.

Dispatch must fail, require review, or require human approval where:

- no required allowed operating area exists;
- no-go-zone overlap exists;
- geometry basis is stale or invalid;
- geometry basis is materially incomplete;
- route corridor conflicts with prohibited/sensitive area;
- spatial scope exceeds authorised mission scope;
- buffer rule is missing where mission class requires buffer;
- geometry mapping from external payload is lossy without acceptable qualification.

A user-interface map, vendor route preview, or adapter payload is not the geofence or no-go-zone law unless it resolves to CP12 mission geometry objects with basis, freshness, and authority posture.

---

## 15. Execution window and temporal coherence

CP12 mission objects must be temporally coherent.

Relevant time objects:

```text
ExecutionWindow
PreflightValidityWindow
DispatchWindow
CommandExpiry
CommandNotBefore
CommandNotAfter
TelemetryTimeBasis
VerificationDeadline
IncidentReviewDeadline
```

Rules:

1. Mission dispatch outside the approved execution window must fail or require re-approval.
2. CommandEnvelope must expire.
3. CommandEnvelope must be replay-protected.
4. Preflight traces must declare validity where used for dispatch.
5. Stale preflight cannot dispatch unless recomputed or explicitly re-approved under policy.
6. Mission dispatch authorisation must expire or be revocable.
7. Mission verification should have a declared deadline where mission class requires timely verification.
8. Temporal contradictions must block dispatch, command signing, or mission completion closure.

Examples of temporal contradictions:

```text
command expiry before dispatch time
preflight validity ending before dispatch
mission execution window closed before command creation
verification deadline before reported completion
ACTIVE dispatch authorization after revocation
```

---

## 16. Mission safety constraints

`MissionSafetyConstraint` is the CP12 object for physical-safety rules that govern mission dispatch and execution.

Mission safety constraint classes may include:

```text
HUMAN_PROXIMITY
ANIMAL_PROXIMITY_INCIDENTAL
PUBLIC_BOUNDARY
ROAD_OR_FOOTPATH
WEATHER_WINDOW
WIND_VISIBILITY_RAIN
SOIL_BEARING_OR_COMPACTION
SLOPE_TERRAIN
OBSTACLE_HANDLING
LOST_LINK_BEHAVIOUR
LOW_POWER_BEHAVIOUR
SENSOR_FAILURE_BEHAVIOUR
SUPERVISION_REQUIRED
EMERGENCY_STOP_REQUIRED
HUMAN_OVERRIDE_REQUIRED
LOCAL_FALLBACK_REQUIRED
REMOTE_TAKEOVER_REQUIRED
COMMAND_INTEGRITY_REQUIRED
GEOFENCE_REQUIRED
NO_GO_ZONE_REQUIRED
```

Constraint strength classes:

```text
HARD_BLOCKING
REVIEW_REQUIRED_FLOOR
HUMAN_APPROVAL_REQUIRED_FLOOR
ADVISORY_WARNING
```

Rules:

- failed hard mission safety constraints block dispatch;
- CP11 charter exception does not override CP12 mission-safety constraints;
- mission safety exceptions require CP12-governed exception or approval path;
- mission safety constraints must declare evidence/freshness basis where material;
- mission safety constraints must not be hidden inside vendor defaults without OFARM-visible trace;
- mission safety controls cannot be disabled by agent tool call, pack activation, or adapter payload alone.

---

## 17. Physical actor capability and compatibility

CP12 defines physical actor capability and compatibility posture.

Physical actor profiles may include:

```text
PhysicalActorCapabilityProfile
RobotCapabilityProfile
MachineCapabilityProfile
ImplementCapabilityProfile
DroneCapabilityProfile
ActuatorCapabilityProfile
SensorTaskingCapabilityProfile
MissionCapabilityRequirement
MissionCapabilityCompatibilityResult
SensorTrustStateForMission
PhysicalActorHealthState
```

Rules:

1. Capability declaration is descriptive, not dispositive.
2. Capability declaration is not authority, dispatch permission, safety proof, or evidence sufficiency.
3. Compatibility must be evaluated for mission class, mission scope, actor, implement/actuator, autonomy level, geometry, environment, time, and policy context.
4. A mission may not dispatch to an unsupported or incompatible physical actor unless a governed exception path exists.
5. Actor capability state may become stale and must be freshness-qualified where material to dispatch.
6. Vendor/manufacturer capability claims remain external evidence or profile material unless accepted into OFARM through governed mapping and currentness rules.

---

## 18. Mission-specific autonomy levels

CP12 defines mission-specific autonomy levels. Autonomy is not global.

Recommended CP12 levels:

```text
M0_RECORD_ONLY
M1_ADVISORY_PLAN
M2_HUMAN_APPROVED_DISPATCH
M3_SUPERVISED_BOUNDED_EXECUTION
M4_POLICY_BOUNDED_EXECUTION
M5_FULLY_AUTONOMOUS_FARM_COORDINATION_OUT_OF_SCOPE
```

Meanings:

| Level | Meaning |
|---|---|
| M0_RECORD_ONLY | OFARM records mission-related material but does not prepare or dispatch. |
| M1_ADVISORY_PLAN | OFARM may prepare advisory mission candidates/plans only. |
| M2_HUMAN_APPROVED_DISPATCH | OFARM may package dispatchable command material only after human approval. |
| M3_SUPERVISED_BOUNDED_EXECUTION | OFARM may support bounded execution under declared supervision, emergency stop, override, fallback, and trace rules. |
| M4_POLICY_BOUNDED_EXECUTION | OFARM may support narrowly bounded execution under explicit policy authority, conformance, telemetry, incident, and downgrade rules. |
| M5_FULLY_AUTONOMOUS_FARM_COORDINATION_OUT_OF_SCOPE | Out of scope for CP12. |

Rules:

- autonomy level must be mission-class-specific;
- autonomy level must be actor-specific;
- autonomy level must be scope/time-specific;
- autonomy level must be revocable;
- autonomy level must be downgradeable;
- software agents cannot self-upgrade autonomy;
- incidents, stale evidence, failed verification, capability failure, revoked authority, pack/profile change, CP11 breach, failed conformance, or safety event may require autonomy downgrade;
- M5 is explicitly out of scope.

CP12 permits mission-envelope law for M0–M4 posture definitions. It does not claim production readiness for any level.

---

## 19. Emergency stop, human override, local fallback, and remote takeover

Cyber-physical mission law must expose safety controls.

CP12 defines:

```text
EmergencyStopPolicy
EmergencyStopActivation
HumanOverridePolicy
LocalFallbackPolicy
LostLinkFallbackPolicy
LowPowerFallbackPolicy
SensorFailureFallbackPolicy
RemoteTakeoverPolicy
RemoteTakeoverEvent
SafeStateDeclaration
AbortAuthority
```

Rules:

1. Dispatchable mission classes must declare emergency-stop posture where physical risk is material.
2. Dispatchable mission classes must declare human-override posture where physical risk is material.
3. Dispatchable mission classes must declare local-fallback posture where connectivity, command, power, sensor, or actor failure could create unsafe behaviour.
4. Emergency stop and human override are safety controls, not ordinary agent tools.
5. Agent-run success, tool success, vendor acknowledgement, or capability manifest does not prove emergency-stop readiness.
6. Missing or insufficient emergency stop, human override, or local fallback posture blocks dispatch for high-risk mission classes.
7. Emergency-stop activation, fallback activation, and remote takeover must produce governed safety records.
8. Remote takeover does not erase the original mission trace; it creates additional control-lineage trace.

---

## 20. Command envelope, command signature, expiry, and replay protection

`CommandEnvelope` is the CP12 dispatchable command package.

A command envelope should bind:

```text
mission envelope ref
mission plan ref
mission dispatch authorization ref
command recipient ref
physical actor ref
mission scope ref
execution window
command expiry
command not-before time
command not-after time
command integrity basis
command signature or equivalent integrity proof
command replay-protection basis
command channel / dispatch surface
external mapping coverage/loss where vendor payload is used
safety and fallback refs
CP11 charter trace refs where material
```

Rules:

1. A command envelope is dispatchable only within declared scope and time.
2. A command envelope must expire.
3. A command envelope must be replay-protected.
4. A command envelope must be bound to recipient or recipient class.
5. A command envelope must be bound to mission dispatch authorisation.
6. A command envelope must not exceed mission scope.
7. Successful API call, tool invocation, adapter submission, command acknowledgement, or channel acknowledgement is not proof of execution.
8. Expired, replayed, unsigned, unbound, or scope-exceeding commands must fail.

---

## 21. Mission dispatch authorisation

`MissionDispatchAuthorization` is the CP12 governance object that permits dispatch for a declared mission scope and time.

It should require:

```text
mission envelope ref
mission plan ref
authority decision trace ref
authorised action class
physical actor ref or class
authorised mission scope
execution window
preflight trace ref
current-state freshness basis where material
CP11 trace ref where material
mission safety policy refs
emergency-stop policy ref
human-override policy ref
local-fallback policy ref
command envelope ref or command preparation basis
authorised approver or policy basis
revocation posture
expiry posture
```

Rules:

- dispatch authorisation is not execution truth;
- dispatch authorisation is not verification;
- dispatch authorisation must be scoped;
- dispatch authorisation must expire or be revocable;
- dispatch authorisation must reference authority trace;
- dispatch authorisation cannot be inferred from mission plan, preflight pass, CP11 pass, actor capability, agent recommendation, tool success, or vendor payload;
- dispatch authorisation cannot expand the mission beyond its preflighted and approved scope unless re-approved.

---

## 22. Agent mission-preparation boundary

Software agents may participate in CP12 only through explicit authority.

When authorised, agents may:

- prepare `MissionCandidate`;
- request mission preflight;
- assemble mission review packages;
- compare mission alternatives;
- explain blocked gates;
- request missing evidence or observation;
- prepare candidate command envelope material;
- draft mission output qualification;
- prepare incident or telemetry review packages.

Agents may not by default:

- approve dispatch;
- sign command envelopes;
- dispatch commands;
- disable emergency stop;
- disable human override;
- disable local fallback;
- self-upgrade autonomy;
- accept mission verification;
- resolve physical safety incidents;
- promote telemetry into accepted execution truth;
- convert vendor payloads into OFARM mission law.

A mission-generating or mission-affecting agent run must link to:

```text
AgentActorshipBinding
AgentAuthorityEnvelope
AgentRunEnvelope
AgentRunTrace
AgentBlockedActionTrace where blocked
MissionCandidate or MissionPlan refs
MissionPreflightTrace where requested
MissionDispatchAuthorization where applicable
AuthorityDecisionTrace where applicable
CP11 SustainabilityPolicyEvaluationTrace where material
```

Handoffs do not transfer mission dispatch authority unless the receiving party/agent has independent authority for the mission action class, scope, and time.

---

## 23. Advisory Twin mission simulation boundary

Mission simulations, route feasibility results, physical actor feasibility forecasts, digital twin previews, predicted execution outcomes, and scenario comparisons belong to the Advisory Twin by default.

They may support:

- mission planning;
- candidate comparison;
- preflight input;
- review packages;
- risk explanation;
- evidence requests;
- blocked-action explanation.

They may not by themselves:

- approve dispatch;
- sign command;
- dispatch command;
- prove command integrity;
- prove execution;
- verify outcome;
- create accepted execution consequences;
- create Compliance Twin facts;
- override mission safety constraints;
- override CP11 charter constraints.

A bridge from advisory mission simulation toward dispatch, command, verified outcome, or Compliance Twin consequence must pass CP12 mission gates and ordinary OFARM authority/evidence/review/promotion law.

---

## 24. Mission telemetry and execution receipt truth boundary

CP12 defines mission telemetry and execution receipt as evidence candidates.

Objects:

```text
MissionTelemetryEnvelope
MachineReportedExecution
OperatorReportedExecution
SensorReportedExecution
MissionExecutionReceipt
TelemetryTrustState
TelemetryCoverageStatement
TelemetryLossMap
CommandAcknowledgement
```

Rules:

1. Telemetry is not accepted truth by import alone.
2. Execution receipt is not verified outcome by report alone.
3. Command acknowledgement is not execution.
4. Machine/vendor telemetry must declare coverage/loss/currentness where material.
5. Telemetry may be spoofed, delayed, partial, lossy, vendor-filtered, or semantically mapped; those limitations must remain visible where used for high-consequence verification.
6. Mission telemetry and execution receipts may support verification, review, evidence sufficiency, and promotion only through governed paths.
7. Telemetry or receipt events may update runtime mission coordination state, but not accepted execution consequences unless governance accepts them.

---

## 25. Mission verification and accepted execution consequences

`MissionVerification` is the CP12 post-mission verification object.

It should include:

```text
mission envelope ref
mission plan ref
command envelope ref where applicable
execution receipt ref
telemetry refs
post-mission observation refs
verification evidence requirement
verification method
verified extent
partial execution extent
deviation from plan
input/application/as-applied evidence where relevant
safety/incident posture
CP11 charter consequence posture where material
result disposition
review/promotion posture
limitations
```

Verification dispositions:

```text
VERIFIED_AS_PLANNED
VERIFIED_WITH_DEVIATION
PARTIAL_VERIFICATION
VERIFICATION_INSUFFICIENT
VERIFICATION_REJECTED
REVIEW_REQUIRED
INCIDENT_REVIEW_REQUIRED
```

Rules:

- `COMPLETED_REPORTED` is not `VERIFIED`;
- verification is not Compliance Twin fact unless promoted;
- verified execution consequences require existing evidence, review, promotion, and current-state law;
- partial execution must remain visible and must not be silently rounded into complete execution;
- mission verification may create evidence for an accepted execution consequence but does not bypass promotion law.

---

## 26. Abort, emergency stop, local fallback, near-miss, and physical safety incident handling

CP12 recognises safety and disruption events as first-class governed records.

Objects/events:

```text
MissionAbortEvent
EmergencyStopActivation
LocalFallbackActivation
LostLinkFallbackActivation
LowPowerFallbackActivation
SensorFailureFallbackActivation
MissionPauseEvent
MissionResumeEvent
RemoteTakeoverEvent
NearMissEvent
PhysicalSafetyIncident
IncidentReviewDecision
IncidentResolution
AutonomyDowngradeRecommendation
MissionClassSuspensionRecommendation
```

Rules:

1. Abort, emergency stop, fallback, pause, resume, and remote takeover events are governed safety records.
2. They may trigger review, evidence needs, mission suspension, autonomy downgrade, authority restriction, actor capability review, output qualification, or incident investigation.
3. Near-miss and physical safety incident records do not automatically create legal or certification compliance facts.
4. Incident records must not disappear into vendor logs.
5. Incident review and resolution require authority trace.
6. Safety incidents may block future mission dispatch for the same actor, mission class, pack/profile, autonomy level, or context until reviewed.
7. Emergency stop and local fallback activation must preserve control-lineage trace where possible.

---

## 27. External vendor, machinery, robot, drone, and tasking payload boundary

External mission, command, telemetry, or tasking payloads are adapter surfaces.

They may come from or be mapped to:

```text
machinery control systems
ISOBUS / ISOXML-like payloads
ADAPT-like operation records
SensorThings-like sensing/tasking payloads
OEM APIs
robot APIs
drone APIs
irrigation controller APIs
contractor/operator systems
telemetry streams
```

Rules:

- external payloads do not define OFARM mission law;
- external command/tasking payloads must map into CP12 command/mission contracts with declared coverage/loss/currentness where material;
- external telemetry payloads must map into CP12 telemetry/receipt contracts with declared coverage/loss/currentness where material;
- vendor command acknowledgement is not execution proof;
- vendor execution log is evidence candidate, not accepted truth;
- adapter mapping must not expand authority, mission scope, command validity, autonomy level, or safety posture;
- loss, ambiguity, or unsupported semantics in vendor mappings must be visible in mission output qualification and preflight where material.

---

## 28. Mission outputs and reporting surfaces

Mission-sensitive outputs must not overstate mission status.

Mission-sensitive outputs include:

```text
mission candidate preview
preflight report
dispatch approval packet
command envelope summary
execution receipt summary
telemetry dashboard
mission verification report
incident summary
near-miss report
partner-facing mission report
submission/reporting assembly
AI-generated mission summary
```

Mission output qualification must expose where material:

```text
mission stage
accepted truth status
preflight result
authority posture
command dispatch status
command acknowledgement status
telemetry coverage/loss
execution receipt status
verification status
incident/near-miss posture
Advisory Twin / Compliance Twin posture
current-state freshness
CP11 charter posture where material
allowed and prohibited downstream use
sharing/redaction/permission posture
limitations
```

Rules:

- a dispatch preview is not executed work;
- a command acknowledgement is not execution;
- an execution receipt is not verification;
- a verification report is not Compliance Twin fact unless promoted;
- an AI-generated mission summary cannot hide stage, truth, verification, or incident limitations.

---

## 29. Mission event grammar and commit matrix implications

CP12 requires a cyber-physical mission event family.

Candidate event names:

```text
MissionCandidateCreated
MissionPreflightRequested
MissionPreflightRecorded
MissionDispatchApproved
MissionDispatchRevoked
MissionCommandEnvelopeCreated
MissionCommandSigned
MissionCommandDispatched
CommandAcknowledged
MissionStarted
MissionPaused
MissionResumed
MissionAbortRequested
MissionAborted
EmergencyStopActivated
LocalFallbackActivated
LostLinkFallbackActivated
RemoteTakeoverActivated
MissionTelemetryReceived
MissionExecutionReceiptReceived
MissionVerificationRecorded
MissionVerificationAccepted
NearMissRecorded
PhysicalSafetyIncidentRecorded
IncidentReviewDecisionRecorded
MissionSuperseded
MissionCancelled
```

Each event must declare:

- event family;
- subject mission;
- producing actor/source;
- event time and recorded time;
- commit class;
- whether it is a note, evidence record, operation claim, governance decision, advisory output, or candidate accepted consequence;
- whether it can influence current-state materialisation only after governance accepts consequences;
- relation to authority trace, evidence, materialisation, or output qualification where material.

Core event rule:

```text
Event presence does not create accepted execution truth, verified outcome, current-state consequence, or Compliance Twin fact by itself.
```

---

## 30. Mission pack/profile surfaces

Mission rules vary by farm, crop, machine class, vendor, terrain, weather, jurisdiction, safety policy, certification scheme, and mission class. Packs may specialise mission policy but may not weaken core CP12 safety law by stealth.

CP12 mission pack surfaces:

```text
MISSION_SAFETY_POLICY
MISSION_AUTONOMY_POLICY
MISSION_GEOFENCE_POLICY
MISSION_COMMAND_INTEGRITY_POLICY
MISSION_VERIFICATION_POLICY
MISSION_TELEMETRY_POLICY
MISSION_INCIDENT_POLICY
MISSION_EXTERNAL_ADAPTER_POLICY
MISSION_EMERGENCY_STOP_POLICY
MISSION_HUMAN_OVERRIDE_POLICY
MISSION_LOCAL_FALLBACK_POLICY
```

Default merge posture:

- safety policies: `STRONGEST_REQUIREMENT` or `HARD_FAIL`;
- autonomy policies: `STRONGEST_REQUIREMENT` or `HARD_FAIL` when conflicting;
- geofence/no-go-zone policies: `CONSTRAINT_INTERSECTION`, `STRONGEST_REQUIREMENT`, or `HARD_FAIL`;
- command-integrity policies: `STRONGEST_REQUIREMENT` or `HARD_FAIL`;
- verification policies: `STRONGEST_REQUIREMENT` or `HARD_FAIL`;
- incident policies: `STRONGEST_REQUIREMENT` or `HARD_FAIL`;
- external adapter policies: `IDENTICAL_ONLY`, `STRONGEST_REQUIREMENT`, or `HARD_FAIL` where meaning/safety is not provably equivalent;
- emergency stop, override, and local fallback policies: `STRONGEST_REQUIREMENT` or `HARD_FAIL`.

Packs may add stricter mission constraints. Packs may not:

- remove emergency-stop requirements;
- remove human-override requirements;
- remove local-fallback requirements;
- downgrade command-integrity requirements;
- expand mission authority;
- self-upgrade autonomy;
- treat vendor payload as hidden mission law;
- turn telemetry into accepted truth;
- bypass CP11 where CP11 applies.

---

## 31. Data sovereignty for mission telemetry and safety records

Mission telemetry, geofence traces, command records, incident logs, near-miss records, verification records, and actor performance records may be commercially, operationally, legally, or safety-sensitive.

Default posture:

```text
mission records are farm-scoped by default unless a valid sharing grant, legal basis, certification obligation, public-authority basis, emergency/safety rule, or explicit governance decision applies.
```

Rules:

- mission telemetry must not be disclosed externally by default;
- near-miss and incident records must not be externally disclosed by default;
- partner/buyer/OEM/insurer disclosure requires explicit sharing basis unless required by law or public-authority process;
- safety review may use mission records inside OFARM under governance;
- CP14 remains responsible for cross-farm mission intelligence, regional hazard exchange, federated robot learning, and benchmark sharing;
- disclosure outputs must carry output qualification, redaction posture, recipient class, purpose, retention, and revocation posture where material.

---

## 32. Interaction with CP11 Sustainable Autonomous Farming Charter

CP12 depends on CP11 but does not replace CP11.

Where a mission materially affects CP11-governed sustainability constraints, objectives, trade-offs, claims, exceptions, or breaches, CP12 must require the applicable CP11 evaluation trace or equivalent charter posture.

CP11 may block, qualify, or route a mission path to review. CP12 then separately evaluates physical mission readiness.

Examples:

| CP11 result | CP12 implication |
|---|---|
| CP11 hard constraint failed | Mission dispatch blocked or review/exception path required. |
| CP11 evidence insufficient | Mission may remain advisory/candidate or require evidence/review. |
| CP11 charter pass | One precondition may be satisfied; dispatch still requires CP12 authority/safety/command gates. |
| CP11 charter exception approved | May satisfy charter exception posture; does not replace mission-safety exception. |
| CP11 sustainability claim basis present | May support mission output claim; does not prove mission execution or verification. |

---

## 33. Interaction with Advisory Twin

Advisory Twin mission material includes:

```text
mission simulations
route feasibility estimates
actor capability forecasts
risk comparisons
scenario results
candidate mission plans
agent-generated mission alternatives
estimated execution outcomes
```

Advisory mission material may inform review, preflight, and planning. It does not create dispatch authority, command integrity, execution proof, verification, current-state consequence, or Compliance Twin fact.

A bridge from Advisory Twin mission material toward dispatch, claim-bearing output, or Compliance Twin consequence must pass:

```text
authority gate
current-state freshness gate
CP11 gate where material
mission preflight gate
mission safety gate
physical actor compatibility gate
command integrity gate
mission verification/promotion gate where outcome is claimed
output qualification gate
```

---

## 34. Interaction with Compliance Twin

CP12 mission material may become relevant to Compliance Twin only through existing governance.

Examples:

- verified execution may support accepted intervention consequence;
- verified as-applied records may support compliance or traceability claims;
- incident review may support nonconformity or corrective-action workflows;
- mission verification limitations may qualify outputs or claims.

Rules:

- command dispatch is not a Compliance Twin fact;
- telemetry is not a Compliance Twin fact by import;
- execution receipt is not a Compliance Twin fact by report;
- near-miss and incident records are not automatically legal/compliance facts;
- verification may support Compliance Twin consequences only through review, promotion, evidence sufficiency, and materialisation law;
- CP12 cannot create autonomous compliance decisioning.

---

## 35. Interaction with current-state materialisation

Mission state, actor state, safety state, telemetry status, and verification posture may be materialised for runtime use.

Such materialisations remain governed current state:

- derived from assertion/history and accepted consequences;
- freshness-qualified;
- purpose-sensitive;
- explainable through basis;
- invalidatable;
- not deeper than assertion/history authority.

Mission dispatch that materially relies on current-state materialisation must prove freshness or route to blocked/review/recompute posture.

A command path must not read stale mission-critical materialisation and silently dispatch.

---

## 36. Interaction with packs

CP12 extends pack law only through mission-specific surfaces. It does not reopen pack merge semantics.

Mission pack surfaces may specialise safety, autonomy, geofence, command integrity, verification, telemetry, incident, external adapter, emergency-stop, human-override, and local-fallback policy.

If mission pack conflicts cannot be resolved deterministically under declared merge mode, the result must hard-fail or require governance. Mission pack conflicts must not silently weaken physical safety, command integrity, authority, geofence, no-go-zone, CP11, current-state, telemetry truth-boundary, or verification rules.

---

## 37. Interaction with agents and capability manifests

Agent and runtime capability manifests may describe CP12 capabilities, but manifests are descriptive.

They do not grant:

- mission dispatch authority;
- command signing authority;
- emergency-stop authority;
- autonomy upgrade authority;
- incident resolution authority;
- verification acceptance authority;
- evidence sufficiency;
- CP11 satisfaction;
- production robot readiness;
- safety certification.

A CP12-capable agent or runtime surface must declare:

- which mission stages it supports;
- which mission action classes it may request or perform;
- whether it can prepare candidates only;
- whether it can request preflight;
- whether it can prepare command candidates;
- whether it can dispatch under any policy-bound class;
- whether dispatch is unsupported;
- trace and blocked-action support;
- safety/control limitations;
- readiness and non-claims.

Default for software agents:

```text
candidate preparation yes if authorised;
preflight request yes if authorised;
dispatch no by default;
command signing no by default;
emergency-stop disabling never;
self-upgrade autonomy never.
```

---

## 38. Interaction with future CP13–CP15

CP12 creates mission-envelope law and explicit hooks, not later-domain law.

### 38.1 CP13 deferral — learning, experimentation, and farm memory

CP12 does not define:

```text
TrialDesign
CausalEstimate
FarmMemoryEntry
LearningPromotionDecision
SeasonalLearningSummary
ExperimentRollbackTrigger
```

Mission records may later become evidence for CP13 learning or farm memory, but CP12 does not promote mission data into learning law by itself.

### 38.2 CP14 deferral — farm-to-farm intelligence

CP12 does not define:

```text
FarmIntelligenceShareGrant
RegionalMissionCoordination
SharedHazardMap
FederatedRobotLearningContribution
BenchmarkDelta
RegionalAlert
```

Mission telemetry and safety records are farm-scoped by default. Cross-farm mission intelligence belongs to CP14.

### 38.3 CP15 deferral — agentic software delivery governance

CP12 does not define:

```text
GeneratedRobotAdapter
RobotDriverDeploymentCandidate
CommandAdapterSBOM
MissionAdapterRollbackPlan
GeneratedSafetyRule
DeploymentCandidate
```

Generated software that affects mission paths must not bypass CP12, but generated-software delivery governance belongs to CP15.

### 38.4 Future livestock-specific mission law

CP12 does not define animal-welfare, livestock proximity, herd/flock, treatment, feeding, movement, or animal-health mission law. Incidental animal proximity may appear as a mission safety constraint, but livestock-specific operational law remains outside the current crop-farming baseline.

---

## 39. Machine-contract implications

CP12 should create draft/non-default machine contracts before any current/default promotion.

Recommended folder:

```text
03_machine_contracts/drafts_non_default/cyber_physical_mission/
```

First-wave CP12 schema candidates:

| Contract | Purpose | Priority |
|---|---|---:|
| `CyberPhysicalMissionEnvelope` | Top-level mission governance container | P0 |
| `MissionIntent` | Desired physical mission objective | P0 |
| `MissionCandidate` | Candidate package for preflight/review | P0 |
| `MissionPlan` | Structured mission package | P0 |
| `MissionScope` | Spatial/temporal/actor/autonomy/safety scope | P0 |
| `MissionPreflightTrace` | No-side-effect mission readiness trace | P0 |
| `MissionDispatchAuthorization` | Scoped/time-bounded dispatch authorisation | P0 |
| `CommandEnvelope` | Dispatchable command package | P0 |
| `CommandIntegrityBasis` | Signature/integrity/replay-protection posture | P0 |
| `MissionSafetyConstraint` | Physical safety constraint | P0 |
| `GeoFence` | Allowed operating area | P0 |
| `NoGoZone` | Prohibited/sensitive operating area | P0 |
| `PhysicalActorCapabilityProfile` | Capability declaration for physical actor | P0 |
| `MissionCapabilityCompatibilityResult` | Actor/mission compatibility result | P0 |
| `AutonomyLevelDeclaration` | Mission-specific autonomy level | P0 |
| `EmergencyStopPolicy` | Stop/safe-state posture | P0 |
| `HumanOverridePolicy` | Override/supervision posture | P0 |
| `LocalFallbackPolicy` | Local failure/safe-state posture | P0 |
| `MissionTelemetryEnvelope` | Telemetry evidence candidate | P1 |
| `MissionExecutionReceipt` | Execution/completion claim | P1 |
| `MissionVerification` | Post-mission verification record | P1 |
| `MissionAbortEvent` | Abort record | P1 |
| `EmergencyStopActivation` | Emergency-stop activation record | P1 |
| `RemoteTakeoverEvent` | Remote takeover record | P1 |
| `NearMissEvent` | Near-miss safety record | P1 |
| `PhysicalSafetyIncident` | Safety incident record | P1 |
| `MissionOutputQualification` | Mission-sensitive output qualification | P1 |
| `MissionPackSurfaceDeclaration` | Mission pack-surface declaration | P2 |

Shared schema requirements:

- JSON Schema 2020-12;
- strict `additionalProperties: false` unless an explicit extension point is declared;
- draft/non-default `$id` and `schemaVersion` until accepted;
- explicit refs rather than hidden runtime state;
- authority/source/freshness/evidence/result enums;
- no implicit current-state mutation;
- no implicit Compliance Twin promotion;
- no implicit agent authority;
- no implicit execution truth;
- no implicit robot/machine readiness claim;
- no implicit CP13/CP14/CP15 semantics.

Required non-authorisation constants for core contracts:

```text
doesNotCreateCanonicalTruth: true
doesNotAuthorizeExecutionByItself: true
doesNotBypassAuthorityLaw: true
doesNotBypassCurrentStateFreshness: true
doesNotBypassCP11WhereApplicable: true
doesNotTreatTelemetryAsAcceptedTruth: true
doesNotTreatReceiptAsVerification: true
doesNotTreatVendorPayloadAsOFARMLaw: true
doesNotCreateComplianceFactByItself: true
```

Command-related contracts should include:

```text
requiresMissionDispatchAuthorization: true
requiresCommandIntegrityBasis: true
requiresExpiry: true
requiresReplayProtection: true
```

Safety-related contracts should include:

```text
emergencyStopRequiredWhereMissionClassRequires: true
humanOverrideRequiredWhereMissionClassRequires: true
localFallbackRequiredWhereMissionClassRequires: true
```

---

## 40. Conformance implications

CP12 must ship with conformance additions. Otherwise it becomes prose at the exact safety boundary that matters most.

Recommended location:

```text
04_implementation_and_conformance/conformance_runners/cyber_physical_mission_conformance/
```

Minimum negative fixtures:

```text
charter_pass_does_not_authorise_mission_dispatch
agent_tool_success_does_not_authorise_dispatch
mission_plan_does_not_authorise_command
mission_preflight_pass_does_not_authorise_dispatch
mission_dispatch_without_authority_trace_fails
mission_dispatch_without_geofence_fails
mission_dispatch_with_no_go_overlap_fails
mission_dispatch_with_expired_execution_window_fails
mission_dispatch_without_emergency_stop_policy_fails
mission_dispatch_without_human_override_policy_fails
mission_dispatch_without_local_fallback_policy_fails
mission_dispatch_with_unsupported_physical_actor_capability_fails
mission_dispatch_with_stale_current_state_fails
mission_dispatch_with_failed_charter_gate_fails
mission_dispatch_with_missing_command_signature_fails
mission_dispatch_with_replayable_command_fails
telemetry_receipt_does_not_create_accepted_execution_truth
command_acknowledgement_does_not_create_execution_truth
execution_receipt_without_verification_cannot_close_mission
mission_simulation_result_does_not_authorise_dispatch
incident_record_does_not_auto_create_compliance_fact
agent_cannot_self_upgrade_autonomy
pack_cannot_weaken_emergency_stop_policy
external_vendor_payload_does_not_define_mission_law
```

Minimum positive fixtures:

```text
valid_supervised_scouting_mission_passes
valid_human_approved_mechanical_weeding_mission_passes
valid_preflight_candidate_without_dispatch_passes
valid_mission_abort_with_emergency_stop_passes
valid_remote_takeover_event_passes
valid_completed_mission_with_verification_passes
valid_agent_prepares_candidate_but_does_not_dispatch_passes
valid_telemetry_receipt_as_evidence_candidate_passes
valid_mission_with_cp11_trace_and_separate_dispatch_authorization_passes
valid_geofenced_mission_with_no_no_go_overlap_passes
valid_command_envelope_with_signature_expiry_and_replay_protection_passes
```

The CP12 runner should be:

- schema-aware;
- semantic-hardening-aware;
- capable of temporal coherence checks;
- capable of geofence/no-go-zone overlap checks or stubbed equivalent for fixtures;
- capable of current-state freshness checks;
- capable of authority-action default checks;
- capable of command expiry/replay checks;
- capable of stage-separation checks;
- capable of telemetry/receipt/verification truth-boundary checks.

---

## 41. Migration notes

CP12 migration should be staged.

### 41.1 Existing planned interventions

Existing `PlannedIntervention` or equivalent planning artifacts should not be automatically treated as `MissionPlan` or dispatchable mission envelopes.

Migration posture:

```text
existing plans may be wrapped as MissionCandidate only where mapping is explicit;
existing plans are not MissionDispatchAuthorization;
existing plans are not CommandEnvelope;
existing plans are not execution truth;
existing plans require mission preflight before any CP12 dispatch path.
```

### 41.2 Existing execution/as-applied records

Existing execution/as-applied records remain under existing intervention/as-applied/evidence law. CP12 may link mission verification to those records when mapping is explicit.

Migration posture:

```text
existing execution records are not CyberPhysicalMissionEnvelope by default;
existing machine imports are telemetry/evidence candidates unless already governed otherwise;
accepted consequences remain governed by existing promotion/materialisation law.
```

### 41.3 Existing telemetry or vendor logs

Existing telemetry/vendor logs should be treated as evidence candidates with coverage/loss/currentness posture where material.

Migration posture:

```text
vendor log ≠ OFARM mission truth;
telemetry stream ≠ verified completion;
command acknowledgement ≠ execution.
```

### 41.4 Existing agent tools

Existing agent tools that prepare interventions, plans, or outputs must not be treated as mission-dispatch-capable unless they are explicitly remapped through CP12 action classes, authority envelopes, and conformance.

### 41.5 Existing packs/profiles

Existing packs that materially affect mission safety, autonomy, geofence, command integrity, verification, telemetry, or external adapter policy should be treated as touching undeclared CP12 surfaces until updated.

---

## 42. Readiness and non-claims

CP12 acceptance would improve OFARM’s model/runtime governance for cyber-physical mission envelopes. It would not prove production robot or machine readiness.

After CP12 acceptance, OFARM may claim:

- bounded model-law support for cyber-physical mission-envelope governance;
- explicit distinction between mission intent, candidate, plan, preflight, dispatch, command, telemetry, receipt, verification, and accepted consequences;
- explicit default-deny mission authority posture;
- explicit CP11 charter precondition interaction for mission paths;
- explicit no-shortcut boundary from plan/preflight/charter pass/agent tool success/vendor payload to dispatch or execution truth;
- draft/non-default machine-contract candidates once schemas are produced;
- conformance fixture support once runners pass.

After CP12 acceptance, OFARM must not claim:

- production robot/machine readiness;
- legal safety certification;
- insurability or liability sufficiency;
- live machine dispatch readiness;
- vendor/OEM integration readiness;
- full autonomous farm operation;
- autonomous compliance decisioning;
- CP13 learning/farm-memory readiness;
- CP14 farm-to-farm intelligence readiness;
- CP15 generated-software delivery readiness;
- livestock-specific mission law;
- external standard conformance unless separately proven;
- that command signatures, telemetry, or execution receipts prove accepted truth by themselves.

Stronger claims require:

- accepted CP12 machine contracts;
- passing CP12 conformance fixtures;
- runtime mission-gate logs;
- trace retrieval evidence;
- current-state freshness enforcement evidence;
- command integrity enforcement evidence;
- emergency stop / human override / local fallback evidence;
- incident-handling evidence;
- actor/vendor adapter mapping coverage/loss evidence;
- human/operator/farmer-facing comprehension validation;
- real-world pilot validation where claims are operational or safety-related.

---

## 43. Risks and open questions

### 43.1 Main risks

| Risk | Severity | Mitigation |
|---|---:|---|
| CP12 becomes robotics product spec | High | Keep mission-envelope boundary; defer vendor protocols. |
| CP12 overclaims robot readiness | High | Add readiness/non-claim addenda. |
| Preflight pass treated as dispatch | Existential | Separate `MissionPreflightTrace` from `MissionDispatchAuthorization`. |
| CP11 charter pass treated as dispatch | Existential | Require separate CP12 dispatch gate. |
| Agent tool success treated as command success | Existential | Require command envelope, dispatch authorisation, and command integrity. |
| Telemetry treated as truth | High | Treat telemetry as evidence candidate only. |
| Command acknowledgement treated as execution | High | Separate acknowledgement from execution receipt and verification. |
| Execution receipt treated as verified outcome | High | Require `MissionVerification`. |
| Geofence/no-go-zone geometry underspecified | High | Add geometry-basis/freshness/conflict rules. |
| Emergency stop/override left to vendor defaults | Existential | Make safety override/fallback posture required. |
| Autonomy level becomes global claim | High | Make autonomy mission-specific, revocable, downgradeable. |
| Mission telemetry leaks commercially sensitive data | High | Default farm-scoped data sovereignty. |
| External payload becomes hidden law | High | Require mapping coverage/loss/currentness. |
| CP12 drifts into CP13/CP14/CP15 | Medium/high | Keep explicit deferrals and non-authorisation constants. |

### 43.2 Open questions

1. Which mission classes should be P0 for CP12 machine contracts?
2. What is the minimal geometry representation needed for first conformance fixtures?
3. Should CP12 define a generic `PhysicalActor` superclass or defer actor taxonomy to machine contracts?
4. How strict should CP12 be for low-risk sensing/scouting missions compared with actuation/treatment missions?
5. What authority defaults should apply to `MISSION_EMERGENCY_STOP` in offline/local contexts?
6. How should mission verification relate to existing `ExecutionRecordPayload` and as-applied records?
7. Which existing machine contracts should CP12 reference versus extend?
8. Which mission-output qualification fields should reuse `ResultQualificationEnvelope` versus define `MissionOutputQualification`?
9. How should CP12 conformance represent geometry overlap without requiring a full geospatial engine?
10. How much external-standard mapping should CP12 include before CP15 generated-adapter law exists?

---

## 44. Acceptance gate

CP12 should not be accepted until all of the following are true:

```text
[ ] RFC scope and non-goals remain bounded to mission-envelope law.
[ ] CP12 does not rewrite truth/current-state/twin/authority/pack/CP11 law.
[ ] Mission stage separation is explicit.
[ ] Mission dispatch authority is separate from preflight, plan, CP11 pass, agent run, command candidate, and vendor payload.
[ ] Command integrity, expiry, and replay protection are required for dispatchable command envelopes.
[ ] Emergency stop, human override, and local fallback posture are required for mission classes where physical risk is material.
[ ] Telemetry and execution receipts remain evidence candidates, not accepted truth.
[ ] Mission verification is required before completed-reported missions can support accepted execution consequences.
[ ] Near-miss and incident records are governed records and do not auto-create compliance facts.
[ ] CP12 machine-contract schemas are staged as draft/non-default until formally promoted.
[ ] CP12 conformance includes both positive and negative fixtures.
[ ] CP12 readiness/non-claims block robot/machine production readiness, safety certification, full autonomy, and live dispatch claims.
[ ] CP13, CP14, CP15, future fleet optimisation, vendor protocol implementation, and livestock-specific law remain deferred.
```

---

## 45. Phase 3 conclusion

This RFC draft establishes CP12 as a controlled cyber-physical mission-envelope extension.

It deliberately does not produce baseline patch text, machine schemas, or conformance fixtures. Those belong to later CP12 phases.

Recommended next phase:

```text
CP12 Phase 4 — Baseline Patch Plan
```

The Phase 4 patch should update only:

```text
00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md
00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md
00_active_baseline/OFARM_Alignment_Register_v0_13.md
00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md
00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md
```

and should not draft machine contracts yet.


---

## 46. Phase 6.1 reconciliation and hardening clauses

This accepted merged incorporates the Phase 6 hostile-review findings and Phase 6.1 remediation package.

The following hardening points are part of the CP12 acceptance posture:

1. **MissionPreflightTrace consistency** — a preflight trace cannot return `PASS` where a blocking check has failed, requires review, requires human approval, or has insufficient basis.
2. **Mission lifecycle stage/reference consistency** — a `CyberPhysicalMissionEnvelope` lifecycle state must be supported by corresponding stage references.
3. **MissionDispatchAuthorization restriction** — dispatch authorisation may approve only mission dispatch or dispatch-command action classes; it cannot authorise telemetry reporting, incident handling, verification, learning, or unrelated action classes.
4. **Temporal coherence** — execution windows, dispatch-validity windows, command-validity windows, command-integrity expiry, and command acknowledgement must be temporally coherent.
5. **Command integrity** — a command integrity basis must cover mission identity, dispatch authorisation, recipient binding, payload digest, expiry, and replay nonce.
6. **Emergency stop and human override** — dispatch-bound missions require applicable emergency-stop, override, local-fallback, lost-link, and remote-takeover posture where the mission class or autonomy level requires them.
7. **Capability compatibility** — dispatch requires a fresh compatibility result against physical-actor capability, safety constraints, command channel, geometry, and execution-window posture.
8. **Geometry validation** — mission scope must not rely on geofence, no-go-zone, route, or geometry basis without a mission geometry validation result where geometry affects dispatch safety.
9. **Mission output qualification** — mission outputs cannot silently become dispatch authority, execution truth, compliance fact, or filed/attested surfaces.
10. **Verification boundary** — mission verification may support accepted execution consequences only through ordinary OFARM evidence, review, promotion, and current-state law.
11. **Conformance requirement** — CP12 acceptance requires both positive and negative executable fixtures, not merely named fixture families.

These hardening clauses do not expand CP12 into CP13, CP14, or CP15. They are enforcement repairs to the CP12 mission-envelope boundary.

## 47. Final candidate currentness posture

The CP12 machine contracts are staged as `drafts_non_default`. They may be used for review, implementation planning, conformance testing, and future currentness promotion, but they are not current/default machine contracts until a separate currentness-promotion decision updates the active machine-contract currentness map.

CP12 may be accepted as an RFC and baseline patch while machine contracts remain draft/non-default if the readiness memo and currentness files preserve that distinction.

## 48. Final acceptance gate

CP12 passes as a accepted merged amendment only if:

- the RFC remains bounded to cyber-physical mission-envelope law;
- the baseline patch does not rewrite OFARM truth, current-state, Advisory/Compliance, authority, pack, agent, or CP11 law;
- schemas remain draft/non-default;
- conformance fixtures pass;
- no production robot/machine readiness claim is made;
- no CP13, CP14, or CP15 law is introduced.


## Phase 7.1 final-gate hardening addendum

Phase 7.1 applies a narrow executable-contract hardening pass. It does not reopen CP12 scope, split CP12, or create CP13, CP14, or CP15 law.

The following hardening rules are part of the CP12 accepted merged amendment:

1. Later mission lifecycle states must preserve upstream chain integrity.
2. A MissionPreflightTrace with `overallDisposition = PASS` must not contain failed, blocked, insufficient-basis, review-required, or human-approval-required results for hard dispatch check classes.
3. MissionOutputQualification must not allow mission reports or advisory outputs to become dispatch authority, accepted execution truth, or compliance facts by ordinary output disposition.
4. CommandEnvelope validity must be bounded by an explicit dispatch-authorisation validity window and by the execution window.
5. EmergencyStopPolicy freshness must not be asserted from future-dated test evidence.
6. CommandEnvelope recipient binding must match the corresponding CommandIntegrityBasis recipient binding under conformance.
7. All CP12 schemas remain draft/non-default until formal currentness promotion.
