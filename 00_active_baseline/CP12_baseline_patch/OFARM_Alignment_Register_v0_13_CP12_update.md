# OFARM Alignment Register v0.13 — CP12 update candidate

Date: 2026-05-28  
Status: final CP12 alignment-register patch candidate; not automatic merge

## CP12 concept rows to add

The following concepts are OFARM-owned or OFARM-governed CP12 concepts. External machinery, robot, drone, tasking, or vendor payload standards may act as anchors, exchange mappings, evidence sources, or adapter profiles only. They do not become hidden OFARM law.

| Concept | Family | Alignment decision | Notes |
|---|---|---|---|
| CyberPhysicalMissionEnvelope | Mission / Runtime / Safety | OFARM_OWNED | Governs mission identity, lifecycle, stage references, and non-authorisation boundaries. |
| MissionIntent | Mission / Planning | OFARM_OWNED | Records physical-mission intent without creating mission authority. |
| MissionCandidate | Mission / Advisory | OFARM_OWNED | Candidate package, often agent-prepared; not dispatch authority. |
| MissionPlan | Mission / Planning | OFARM_OWNED | Governed plan; not command. |
| MissionScope | Mission / Geometry / Context | OFARM_OWNED | Declares mission spatial/temporal/actor/policy scope. |
| MissionPreflightTrace | Mission / Runtime / Safety | OFARM_OWNED | Preflight gate result; not dispatch authority. |
| MissionDispatchAuthorization | Mission / Authority | OFARM_OWNED | Action-specific authority record for dispatch. |
| CommandEnvelope | Mission / Command | OFARM_OWNED | Bounded command wrapper; not execution truth. |
| CommandIntegrityBasis | Mission / Security | OFARM_OWNED | Payload, recipient, mission, expiry, and replay-protection binding. |
| CommandAcknowledgement | Mission / Evidence | OFARM_OWNED | Command receipt acknowledgement; not proof of execution. |
| ExecutionWindow | Mission / Time | OFARM_OWNED | Temporal bounds for dispatch and command validity. |
| GeoFence | Mission / Geometry | OFARM_OWNED | Positive allowed mission boundary. |
| NoGoZone | Mission / Geometry / Safety | OFARM_OWNED | Excluded spatial area or condition. |
| RouteConstraint | Mission / Geometry / Safety | OFARM_OWNED | Route/path constraint for mission planning. |
| MissionGeometryValidationResult | Mission / Geometry / Safety | OFARM_OWNED | Validates geofence/no-go/route/CRS/freshness basis. |
| MissionSafetyConstraint | Mission / Safety | OFARM_OWNED | Safety constraint; critical classes cannot be advisory only. |
| PhysicalActorCapabilityProfile | Mission / Capability | OFARM_OWNED | Declared/verified capability of robot, machine, actuator, drone, or physical actor. |
| MissionCapabilityCompatibilityResult | Mission / Capability / Safety | OFARM_OWNED | Fresh compatibility result required for dispatch-bound missions. |
| AutonomyLevelDeclaration | Mission / Autonomy | OFARM_OWNED | Mission-specific autonomy declaration; does not grant authority by itself. |
| EmergencyStopPolicy | Mission / Safety | OFARM_OWNED | Emergency-stop availability, freshness, and test-evidence posture. |
| HumanOverridePolicy | Mission / Safety | OFARM_OWNED | Human-supervision and override posture. |
| LocalFallbackPolicy | Mission / Safety | OFARM_OWNED | Local fallback behaviour where connectivity/controller path fails. |
| LostLinkPolicy | Mission / Safety | OFARM_OWNED | Lost-link behaviour for mission-bound physical actors. |
| RemoteTakeoverEvent | Mission / Safety / Event | OFARM_OWNED | Remote takeover event; not accepted execution truth by itself. |
| MissionTelemetryEnvelope | Mission / Evidence | OFARM_OWNED | Machine-reported telemetry wrapper; evidence candidate only. |
| MissionExecutionReceipt | Mission / Evidence | OFARM_OWNED | Execution receipt; not verification by itself. |
| MissionVerification | Mission / Verification | OFARM_OWNED | Verification record; promotion still follows OFARM evidence/review law. |
| MissionAbortEvent | Mission / Event / Safety | OFARM_OWNED | Records abort/fallback event. |
| NearMissEvent | Mission / Event / Safety | OFARM_OWNED | Near-miss record requiring review for high-severity cases. |
| PhysicalSafetyIncident | Mission / Event / Safety | OFARM_OWNED | Physical safety incident record; not compliance fact by itself. |
| MissionOutputQualification | Mission / Output | OFARM_OWNED | Qualifies mission outputs and blocks misuse. |

## Residual debt

- CP12 schemas remain draft/non-default.
- External vendor payload profiles are not current/default.
- Safety certification is not claimed.
- Production robot/machine readiness is not claimed.
