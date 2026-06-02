# CP12 Phase 6 — Hostile Review

Status: hostile review of CP12 RFC draft, Phase 4 baseline patch plan, Phase 5 machine-contract plan, Phase 5 draft schemas, and Phase 5 conformance fixture plan.  
Review date: 2026-05-28  
Recommendation: **ACCEPT WITH CHANGES**.

## 0. Executive verdict

```text
CP12 direction: PASS
CP12 boundary: PASS
CP12 no-split decision: PASS
CP12 draft/non-default staging: PASS
CP12 schema enforceability: PARTIAL FAIL
CP12 conformance posture: FAIL — fixture plan only, no executable runner
Acceptance recommendation: ACCEPT WITH CHANGES
Do not merge CP12 yet.
Do not promote CP12 schemas to current/default.
Do not proceed to CP13, CP14, or CP15 from CP12 until CP12 remediation passes.
```

CP12 is the right amendment. It addresses a real missing executable contract: the boundary between approved operational intent and physical mission dispatch. It correctly avoids becoming a robotics product specification, fleet optimiser, vendor protocol layer, legal safety certification, or full autonomy system.

The RFC and baseline patch say the right thing:

```text
recommendation / mission plan / preflight pass / CP11 charter pass / agent tool success / command acknowledgement / telemetry receipt
≠ physical mission authority
≠ execution truth
≠ accepted consequence
```

The hostile finding is that the draft machine contracts are not yet strict enough to enforce that invariant. Several critical safety and authority states are present as fields, but their cross-field consistency is not yet mechanically enforced.

The amendment should continue. It should not be split. The next step should be **CP12 Phase 6.1 — Remediation Pass**, focused on schema hardening and executable conformance.

---

## 1. Direct answers to the hostile-review checks

| Check | Verdict | Notes |
|---|---|---|
| 1. Contradicts existing OFARM truth law? | **No.** | CP12 preserves assertion/history-first truth and says telemetry, receipts, acknowledgement, and verification do not self-promote. |
| 2. Preserves stage separation? | **Conceptually yes; schema partially.** | The RFC distinguishes intent/candidate/plan/preflight/dispatch/command/ack/telemetry/receipt/verification. The top-level envelope schema does not yet enforce lifecycle-required references. |
| 3. Lets preflight success become dispatch authority? | **Text says no; schema needs hardening.** | `MissionPreflightTrace` has `doesNotAuthorizeDispatch: true`, but `PASS` can coexist with failed checks. |
| 4. Lets acknowledgement or telemetry become execution truth? | **Mostly no.** | Guardrail constants are strong. But verification/receipt relations still need more consistency checks. |
| 5. Lets agents become hidden physical governors? | **Risk remains.** | `MissionCandidate.agentRunTraceRef` is optional and there is no conditional enforcement when candidate preparation is agentic. |
| 6. Authorises robot/machine execution without human or bounded policy authority? | **Possible schema gap.** | `MissionDispatchAuthorization` requires authority trace, but the authorised action class is too broad and temporal/state checks are incomplete. |
| 7. Preserves CP11 charter gates? | **Text yes; schema under-enforced.** | `cp11CharterTraceRefs` can be empty even for mission classes likely to affect sustainability constraints. Need applicability state. |
| 8. Defines geofence/no-go/geometry enough for conformance? | **No.** | It references geometry, but no geometry-relation result object exists. Overlap/containment remains only a future conformance idea. |
| 9. Defines command integrity enough? | **Partially.** | Signature, nonce, recipient binding, and expiry exist. Temporal coherence and payload digest binding are under-specified. |
| 10. Defines emergency stop / override / fallback enough? | **Partially.** | Policy objects exist, but test/freshness/readiness and risk-class applicability are under-enforced. |
| 11. Requires current-state freshness for dispatch? | **Mostly yes.** | Dispatch authorization requires `FRESH` for approved/active states. Mission plans/scope still need clearer relationship to dispatch. |
| 12. Preserves Advisory/Compliance split? | **Yes.** | The conceptual boundary is sound. Verification and incident records still need better promotion-state guards. |
| 13. Enough conformance? | **No.** | Phase 5 provides a fixture plan only. No executable runner, input fixtures, expected outputs, or adversarial cases. |
| 14. OFARM machine-contract style? | **Mostly yes.** | JSON Schema 2020-12, `additionalProperties: false`, draft/non-default IDs, references, guardrail constants, and examples are consistent with OFARM style. |
| 15. Any schemas accidentally implementing CP13–CP15? | **No.** | CP12 stays within cyber-physical mission envelope law. No experimentation, farm-intelligence, or generated-software contracts are created. |

---

## 2. Top defects

## Defect 1 — `MissionDispatchAuthorization.authorisedActionClass` is too broad

**Severity:** High  
**Blocking for final CP12 package:** Yes

`MissionDispatchAuthorization` can currently carry action classes that are not dispatch approval or dispatch command, such as:

```text
MISSION_REPORT_TELEMETRY
MISSION_ACKNOWLEDGE_COMMAND
MISSION_RECORD_NEAR_MISS
MISSION_RECORD_PHYSICAL_SAFETY_INCIDENT
```

An adversarial instance with:

```json
"authorisedActionClass": "MISSION_REPORT_TELEMETRY"
```

passed schema validation.

### Why it matters

A dispatch-authorisation object should not authorise unrelated mission actions. This blurs reporting, acknowledgement, incident recording, and physical dispatch authority.

### Required fix

Restrict `MissionDispatchAuthorization.authorisedActionClass` to:

```text
MISSION_APPROVE_DISPATCH
MISSION_DISPATCH_COMMAND
```

If CP12 needs authorisation objects for abort, emergency stop, remote takeover, verification acceptance, or incident resolution, create separate action-specific authorisation contexts or a more general `MissionAuthorityDecisionBinding`. Do not overload `MissionDispatchAuthorization`.

### Required fixtures

```text
mission_dispatch_authorization_with_telemetry_action_class_fails
mission_dispatch_authorization_with_incident_action_class_fails
valid_mission_dispatch_authorization_with_dispatch_action_passes
```

---

## Defect 2 — Mission preflight can pass despite failed or blocking checks

**Severity:** High  
**Blocking for final CP12 package:** Yes

`MissionPreflightTrace` allows:

```json
{
  "overallDisposition": "PASS",
  "checkResults": [
    {"checkClass": "GEOMETRY", "result": "FAIL", "blocking": true}
  ]
}
```

This passed schema validation when shaped with the declared `checkResults` object.

### Why it matters

Preflight is the main guard between plan and dispatch. It must not pass when a blocking check failed.

### Required fix

Add schema or semantic conformance rule:

```text
If any checkResult has blocking = true and result in [FAIL, BLOCKED, INSUFFICIENT_BASIS, REQUIRE_REVIEW, REQUIRE_HUMAN_APPROVAL], then overallDisposition must not be PASS.
```

Also:

```text
If overallDisposition = PASS, all blocking check results must be PASS.
```

### Required fixtures

```text
preflight_pass_with_blocking_geometry_failure_fails
preflight_pass_with_blocking_safety_failure_fails
preflight_pass_with_insufficient_basis_fails
valid_preflight_pass_with_all_blocking_checks_passed_passes
valid_preflight_requires_review_with_blocking_review_check_passes
```

---

## Defect 3 — Temporal coherence is not enforced for execution windows, commands, command integrity, and dispatch authorisation

**Severity:** High  
**Blocking for final CP12 package:** Yes

The following adversarial cases pass schema validation:

```text
ExecutionWindow.notAfter < ExecutionWindow.notBefore
CommandEnvelope.notAfter < CommandEnvelope.notBefore
CommandIntegrityBasis.expiresAt < createdAtCommandTime
MissionDispatchAuthorization.validUntil < validFrom
```

### Why it matters

Temporal incoherence is a direct cyber-physical safety problem. Expired or inverted windows can create replay, stale command, or unauthorised execution hazards.

### Required fix

JSON Schema cannot easily compare date-time values. Add semantic conformance checks:

```text
ExecutionWindow.notAfter must be after notBefore.
CommandEnvelope.notAfter must be after notBefore.
CommandIntegrityBasis.expiresAt must be after createdAtCommandTime.
MissionDispatchAuthorization.validUntil must be after validFrom.
CommandEnvelope validity must be inside or equal to the referenced ExecutionWindow and DispatchAuthorization window.
CommandIntegrityBasis expiry must not exceed CommandEnvelope.notAfter unless a stricter policy explicitly allows it.
```

### Required fixtures

```text
execution_window_inverted_time_fails
command_envelope_inverted_time_fails
command_integrity_expiry_before_created_fails
dispatch_authorization_inverted_validity_fails
command_envelope_outside_execution_window_fails
valid_command_temporal_chain_passes
```

---

## Defect 4 — Mission lifecycle state is not linked to required stage references

**Severity:** High  
**Blocking for final CP12 package:** Yes

`CyberPhysicalMissionEnvelope` allows states inconsistent with stage references. For example:

```json
"missionLifecycleState": "DISPATCHED",
"commandEnvelopeRefs": []
```

passed schema validation.

### Why it matters

The envelope is the top-level mission governance container. If it can claim `DISPATCHED`, `ACKNOWLEDGED`, `IN_PROGRESS`, `COMPLETED_REPORTED`, `VERIFIED`, or `CLOSED` without the corresponding stage references, stage separation becomes documentary rather than executable.

### Required fix

Add conditional requirements:

```text
if missionLifecycleState = CANDIDATE -> require missionCandidateRef
if missionLifecycleState = PLANNED -> require missionPlanRef
if missionLifecycleState = PREFLIGHTED -> require missionPreflightTraceRefs minItems 1
if missionLifecycleState = AUTHORISED -> require missionDispatchAuthorizationRefs minItems 1
if missionLifecycleState = COMMAND_PACKAGED or DISPATCHED -> require commandEnvelopeRefs minItems 1
if missionLifecycleState = ACKNOWLEDGED -> require commandAcknowledgementRefs minItems 1
if missionLifecycleState = IN_PROGRESS -> require commandEnvelopeRefs and telemetryEnvelopeRefs or executionReceiptRefs according to policy
if missionLifecycleState = COMPLETED_REPORTED -> require executionReceiptRefs minItems 1
if missionLifecycleState = VERIFIED -> require missionVerificationRefs minItems 1
if missionLifecycleState = CLOSED -> require missionVerificationRefs or closureReviewDecisionRef
if missionLifecycleState = ABORTED -> require abort or emergency-stop event reference
```

### Required fixtures

```text
mission_envelope_dispatched_without_command_fails
mission_envelope_verified_without_verification_fails
mission_envelope_completed_without_receipt_fails
valid_dispatched_mission_with_command_ref_passes
valid_verified_mission_with_verification_ref_passes
```

---

## Defect 5 — Command payload integrity binding is under-specified

**Severity:** High  
**Blocking for final CP12 package:** Yes

`CommandEnvelope` references a `commandPayloadRef` and a `CommandIntegrityBasis`, but does not require a digest/hash or explicit statement that the signature covers the exact command payload, mission, recipient, expiry, and dispatch authorisation.

### Why it matters

A command can be syntactically signed while the exact payload binding is unclear. Cyber-physical command integrity needs explicit anti-substitution semantics.

### Required fix

Add to `CommandIntegrityBasis` or `CommandEnvelope`:

```text
commandPayloadDigestRef or commandPayloadHash
signatureCovers:
  - commandPayload
  - missionEnvelopeRef
  - missionDispatchAuthorizationRef
  - recipientActorRef
  - notBefore
  - notAfter
  - replayProtectionNonce
```

Require `signatureCovers` to include all required binding elements unless `integrityMethod` has a formally declared equivalent.

### Required fixtures

```text
command_integrity_missing_payload_digest_fails
command_integrity_signature_does_not_cover_recipient_fails
command_integrity_signature_does_not_cover_expiry_fails
valid_command_integrity_full_binding_passes
```

---

## Defect 6 — Emergency stop policy is not freshness/test gated

**Severity:** High  
**Blocking for final CP12 package:** Yes for mission-dispatch readiness claims

`EmergencyStopPolicy` requires:

```text
availableDuringMission: true
notOrdinaryAgentTool: true
```

That is good. But `testEvidenceRefs` and `lastTestedAt` are optional.

### Why it matters

A stale or untested emergency stop policy should not support mission dispatch, especially for material physical risk or high-risk actuation.

### Required fix

Add either:

```text
EmergencyStopReadiness
```

or harden `EmergencyStopPolicy` with:

```text
testEvidenceRefs minItems 1 for dispatch-bound use
lastTestedAt required for dispatch-bound use
readinessFreshnessState: FRESH | STALE_BLOCKING | UNKNOWN_BLOCKING
```

Dispatch authorisation should require emergency-stop readiness to be fresh for:

```text
MATERIAL_PHYSICAL_RISK
HIGH_RISK_ACTUATION
M3_SUPERVISED_BOUNDED_EXECUTION
M4_POLICY_BOUNDED_EXECUTION
```

### Required fixtures

```text
mission_dispatch_with_untested_emergency_stop_policy_fails
mission_dispatch_with_stale_emergency_stop_readiness_fails
valid_dispatch_with_fresh_emergency_stop_readiness_passes
```

---

## Defect 7 — Human override and supervision are under-enforced for high-risk autonomy

**Severity:** High  
**Blocking for final CP12 package:** Yes

`HumanOverridePolicy.supervisionRequired` is optional. `AutonomyLevelDeclaration` allows M3/M4 declarations with authority trace, but no clear conditional rule tying high-risk autonomy to supervision/override freshness.

### Why it matters

M3/M4 autonomy with weak supervision is exactly the kind of hidden physical governance CP12 is supposed to prevent.

### Required fix

Add conditional rule:

```text
If declaredAutonomyLevel in [M3_SUPERVISED_BOUNDED_EXECUTION, M4_POLICY_BOUNDED_EXECUTION], then require:
- humanOverridePolicyRef or equivalent binding in MissionDispatchAuthorization
- supervisionRequired = true or explicitly justified policy exception
- authorityDecisionTraceRef
- downgrade path
- emergency stop policy
- local fallback policy
```

For `HIGH_RISK_ACTUATION`, require human approval unless a future RFC explicitly narrows the rule.

### Required fixtures

```text
m3_autonomy_without_supervision_fails
m4_autonomy_without_explicit_policy_authority_fails
high_risk_actuation_without_human_override_fails
valid_m3_supervised_autonomy_passes
```

---

## Defect 8 — Physical capability compatibility can be too weak

**Severity:** High

`PhysicalActorCapabilityProfile` can declare `capabilityState = VERIFIED` without requiring:

```text
lastVerifiedAt
safetyControlRefs
commandChannelRefs
```

`MissionCapabilityCompatibilityResult` can return `COMPATIBLE` without requiring safety-control checks or current capability freshness.

### Why it matters

A verified capability must be time-bounded and evidence-backed. Otherwise a robot or machine can be treated as compatible because a static profile says so.

### Required fix

Add conditional rules:

```text
if capabilityState = VERIFIED -> require lastVerifiedAt, safetyControlRefs, commandChannelRefs
if capabilityState in [STALE, REVOKED, UNKNOWN_BLOCKING] -> compatibilityDisposition cannot be COMPATIBLE
if compatibilityDisposition = COMPATIBLE -> require checkedSafetyConstraintRefs minItems 1 for material-risk/high-risk missions
```

### Required fixtures

```text
verified_capability_without_last_verified_at_fails
compatible_result_with_stale_capability_fails
high_risk_compatible_result_without_safety_check_fails
valid_verified_capability_profile_passes
```

---

## Defect 9 — CP11 charter-gate applicability is under-modelled

**Severity:** High

`MissionScope`, `MissionIntent`, `MissionPlan`, and `MissionDispatchAuthorization` include `cp11CharterTraceRefs`, but these arrays may be empty. There is no field declaring whether CP11 is applicable, not applicable, already satisfied, blocked, or unknown.

### Why it matters

CP12 must not treat CP11 charter pass as dispatch authority. But it also must not allow charter-sensitive missions to dispatch without a CP11 gate.

### Required fix

Add a CP11 applicability state, for example:

```text
cp11ApplicabilityState:
  APPLICABLE_TRACE_REQUIRED
  NOT_APPLICABLE_WITH_REASON
  UNKNOWN_BLOCKING
```

If `APPLICABLE_TRACE_REQUIRED`, require `cp11CharterTraceRefs minItems 1`.

If `NOT_APPLICABLE_WITH_REASON`, require `cp11NotApplicableReason`.

If `UNKNOWN_BLOCKING`, dispatch/preflight pass must fail.

### Required fixtures

```text
charter_applicable_mission_without_cp11_trace_fails
charter_unknown_blocking_prevents_dispatch_fails
valid_non_charter_applicable_mission_with_reason_passes
valid_charter_applicable_mission_with_trace_passes
```

---

## Defect 10 — Mission safety constraints permit advisory-only safety warnings

**Severity:** Medium/high

`MissionSafetyConstraint.constraintStrength` allows:

```text
ADVISORY_WARNING
```

This is not always wrong, but it is risky inside a `MissionSafetyConstraint` object. For physical safety, certain classes should never be advisory-only.

### Why it matters

`EMERGENCY_STOP_REQUIRED`, `HUMAN_OVERRIDE_REQUIRED`, `LOCAL_FALLBACK_REQUIRED`, `COMMAND_INTEGRITY_REQUIRED`, `GEOFENCE_REQUIRED`, and `NO_GO_ZONE_REQUIRED` should not become advisory warnings in dispatch-bound missions.

### Required fix

Add conditional rules:

```text
If constraintClass in [EMERGENCY_STOP_REQUIRED, HUMAN_OVERRIDE_REQUIRED, LOCAL_FALLBACK_REQUIRED, COMMAND_INTEGRITY_REQUIRED, GEOFENCE_REQUIRED, NO_GO_ZONE_REQUIRED], then constraintStrength must be HARD_BLOCKING or HUMAN_APPROVAL_REQUIRED_FLOOR.
```

For advisory warnings, use a separate `MissionHazardAdvisory` or require non-dispatch/advisory-only posture.

### Required fixtures

```text
emergency_stop_required_as_advisory_warning_fails
command_integrity_required_as_advisory_warning_fails
valid_hard_blocking_emergency_stop_constraint_passes
```

---

## Defect 11 — Geofence/no-go-zone geometry relation is not executable enough

**Severity:** High

CP12 references geofences and no-go zones, but there is no machine contract for the geometry relation result, such as:

```text
mission route contained within geofence
mission route overlaps no-go zone
geometry freshness verified
coordinate reference systems compatible
lossy vendor geometry mapping detected
```

### Why it matters

“Has a geofence ref” is not enough. A mission can have both a geofence and a no-go zone and still violate it.

### Required fix

Add a draft contract:

```text
MissionGeometryValidationResult
```

Minimum fields:

```text
missionScopeRef
geoFenceRefs
noGoZoneRefs
routeOrCoverageGeometryRef
crsCompatibilityState
geometryFreshnessState
containmentResult
overlapResult
mappingCoverageRef
lossMapRef
blocking
resultDisposition
```

### Required fixtures

```text
mission_dispatch_with_no_go_overlap_fails
mission_dispatch_with_crs_mismatch_fails
mission_dispatch_with_stale_geofence_fails
valid_geofence_containment_without_no_go_overlap_passes
```

---

## Defect 12 — Mission output qualification can allow contradictory dispositions and uses

**Severity:** Medium/high

`MissionOutputQualification` does not enforce enough consistency between:

```text
outputDisposition
allowedUseClasses
blockedUseClasses
```

An adversarial case with:

```text
outputDisposition = ADVISORY_ONLY
allowedUseClasses = [FILED_SUBMISSION]
```

passed schema validation.

### Why it matters

Mission outputs can become operational reports, claims, attestations, or filings. Output qualification must not allow an advisory-only output to be filed or treated as claim-bearing.

### Required fix

Add conditional rules:

```text
if outputDisposition = ADVISORY_ONLY -> blockedUseClasses must include CLAIM_BEARING_OUTPUT, ATTESTATION_CANDIDATE, FILED_SUBMISSION, DISPATCH_AUTHORITY, EXECUTION_TRUTH, COMPLIANCE_FACT
if outputDisposition = MISSION_REPORT -> allowedUseClasses may include MISSION_REPORT but not FILED_SUBMISSION unless separately qualified
if outputDisposition = FILED_SUBMISSION -> require authorityDecisionTraceRef / filingBasisRef in a future output contract
```

Also add no-overlap rule where the same use can appear in both allowed and blocked sets, if later enums converge.

### Required fixtures

```text
advisory_mission_output_with_filed_submission_use_fails
advisory_mission_output_with_claim_bearing_use_fails
valid_mission_report_output_passes
```

---

## Defect 13 — Mission verification can be semantically inconsistent

**Severity:** Medium/high

`MissionVerification` allows:

```text
verificationDisposition = FAILED_VERIFICATION
acceptedConsequenceCandidateRefs = [ ... ]
```

and also allows:

```text
verificationDisposition = VERIFIED_AS_REPORTED
acceptedConsequenceCandidateRefs = []
```

The latter may be acceptable if verification is only a verification record, but the former is unsafe.

### Why it matters

Accepted-consequence candidates should not be generated from failed verification without explicit review or exception semantics.

### Required fix

Add conditional rules:

```text
if verificationDisposition in [FAILED_VERIFICATION, NOT_VERIFIED, DISPUTED] -> acceptedConsequenceCandidateRefs must be empty or absent
if verificationDisposition = VERIFIED_AS_REPORTED and acceptedConsequenceCandidateRefs is empty -> require noAcceptedConsequencesReason
```

### Required fixtures

```text
failed_verification_with_accepted_consequence_candidate_fails
verified_as_reported_without_consequence_or_reason_fails
valid_verified_with_consequence_candidate_passes
valid_failed_verification_without_consequence_candidate_passes
```

---

## Defect 14 — Agent mission-preparation boundary is not mechanically enforceable

**Severity:** High

`MissionCandidate` includes optional `agentRunTraceRef`, but there is no field indicating whether the candidate was prepared by a software agent. Therefore the schema cannot require an agent-run trace when agentic preparation occurred.

### Why it matters

A software agent could prepare a mission candidate while the package looks human-prepared or untraceable. That weakens the agent-boundary law.

### Required fix

Add:

```text
preparedByActorClass:
  HUMAN
  SOFTWARE_AGENT
  SERVICE
  MACHINE_IMPORTED
```

If `preparedByActorClass = SOFTWARE_AGENT`, require:

```text
agentRunTraceRef
agentAuthorityEnvelopeRef
agentBlockedActionTraceRefs if any blocked actions occurred
```

Also require `doesNotAuthorizeDispatch: true` as already present.

### Required fixtures

```text
agent_prepared_candidate_without_run_trace_fails
agent_prepared_candidate_without_authority_envelope_fails
valid_agent_prepared_candidate_with_run_trace_passes
```

---

## Defect 15 — Dispatch and command objects do not prove consistency with physical actor compatibility

**Severity:** High

`MissionDispatchAuthorization` requires `physicalActorRefs`, but does not require a `MissionCapabilityCompatibilityResult`. `CommandEnvelope` binds to a recipient but does not require proof that the recipient is compatible with the mission class, autonomy level, safety constraints, and command channel.

### Why it matters

A mission can be authorised and commanded to a physical actor that is not proven capable or compatible.

### Required fix

Add to `MissionDispatchAuthorization`:

```text
capabilityCompatibilityResultRefs minItems 1
```

For high-risk missions, compatibility results must be `COMPATIBLE` and fresh.

Add to `CommandEnvelope`:

```text
recipientCapabilityCompatibilityRef
```

or require the dispatch authorisation to bind recipient compatibility.

### Required fixtures

```text
dispatch_without_capability_compatibility_result_fails
command_to_unverified_actor_fails
valid_dispatch_with_compatible_actor_passes
```

---

## Defect 16 — Command acknowledgement timestamp and command validity are not semantically linked

**Severity:** Medium

A `CommandAcknowledgement` can acknowledge a command after its `notAfter` expiry, because it only references the command envelope.

### Why it matters

Late acknowledgement should not be treated as a usable operational signal.

### Required fix

Semantic conformance should check:

```text
acknowledgedAt must fall within or be consistent with CommandEnvelope validity.
If acknowledgedAt is after notAfter, acknowledgementState must be EXPIRED_REJECTED or equivalent.
```

### Required fixtures

```text
command_acknowledged_after_expiry_as_received_fails
expired_command_acknowledged_as_expired_rejected_passes
```

---

## Defect 17 — Mission pack support is only a hook

**Severity:** Medium

`MissionPackSurfaceDeclaration` exists, but active pack merge contracts are not amended. This is acceptable for Phase 5 draft posture, but it must be clearly labelled.

### Required fix

Either draft patched versions of:

```text
PackActivationSet
PackMergeResolutionTrace
PackSurfaceFamily
```

or explicitly mark mission-pack support as draft/non-default and not executable until pack currentness is updated.

### Required fixtures

```text
pack_cannot_weaken_emergency_stop_policy
pack_cannot_create_dispatch_authority
conflicting_mission_pack_surfaces_hard_fail
```

---

## Defect 18 — Conformance is a plan, not executable evidence

**Severity:** High  
**Blocking for final CP12 package:** Yes

Phase 5 includes a conformance fixture plan, but no executable runner, fixture inputs, expected outputs, or results.

### Why it matters

CP12 is cyber-physical safety law. A list of fixture names is not enough.

### Required fix

Create a schema-aware and semantic-hardening-aware runner with positive and negative fixtures.

Minimum fixture families:

```text
stage separation
preflight result consistency
dispatch authority
temporal coherence
command integrity
CP11 applicability
geofence/no-go relation
emergency stop readiness
human override / autonomy
capability compatibility
telemetry/receipt/verification truth boundary
incident/non-compliance boundary
agent preparation boundary
pack safety boundary
```

---

# 3. What CP12 got right

CP12 is directionally strong.

It correctly establishes:

```text
- mission dispatch is not produced by intent, plan, preflight, charter pass, agent confidence, tool success, capability declaration, telemetry, receipt, or vendor payload;
- mission stage separation is necessary;
- command integrity, recipient binding, expiry, and replay protection are first-class;
- emergency stop, human override, local fallback, and remote takeover are mission-law objects;
- telemetry and execution receipts are evidence candidates only;
- verification still does not bypass review/promotion law;
- physical safety incidents and near misses do not automatically create compliance facts;
- CP12 does not create CP13, CP14, or CP15 law;
- CP12 does not claim production robot readiness.
```

The draft/non-default staging is also correct.

---

# 4. Does CP12 need to be split?

No.

CP12 is coherent as one amendment:

```text
cyber-physical mission envelope law
```

Splitting now would increase coordination cost without solving the actual defects. The defects are schema/conformance hardening issues, not scope failure.

Keep the split already established:

```text
CP12 — cyber-physical mission envelope
CP13 — learning, experimentation, farm memory
CP14 — farm-to-farm intelligence
CP15 — agentic software delivery governance
```

---

# 5. Required fixes before Phase 7

## P0 — Blocking fixes

```text
1. Restrict MissionDispatchAuthorization authorisedActionClass.
2. Enforce preflight overallDisposition consistency with checkResults.
3. Add temporal-coherence checks for execution windows, command windows, integrity expiry, and dispatch validity.
4. Enforce mission lifecycle state/reference consistency in CyberPhysicalMissionEnvelope.
5. Add command payload digest / signature-coverage binding.
6. Require emergency-stop readiness/test freshness for dispatch-bound missions.
7. Enforce human override/supervision requirements for M3/M4 and high-risk actuation.
8. Require capability compatibility results for dispatch/command.
9. Add CP11 applicability state and required trace rules.
10. Add geometry validation result for geofence/no-go/route relation.
11. Harden MissionOutputQualification dispositions and allowed uses.
12. Make conformance executable, not just planned.
```

## P1 — Strongly recommended fixes

```text
13. Add verification disposition consistency rules.
14. Add agent-prepared mission candidate trace requirements.
15. Add command acknowledgement validity-window checks.
16. Keep mission-pack support explicitly draft/non-default unless pack contracts are patched.
17. Clarify safety constraint classes that cannot be advisory warnings.
18. Add more explicit data-sovereignty posture for telemetry and incident records.
```

## P2 — Can remain open but must be recorded

```text
19. Real-world robot/vendor protocol mapping.
20. Legal/safety certification review.
21. Field pilot evidence.
22. Human factors validation for emergency stop and remote takeover UX.
23. Insurance/liability interpretation.
24. Livestock-specific robot/animal-welfare mission variants.
```

---

# 6. Revised CP12 acceptance gate

CP12 can pass hostile review only when:

```text
[ ] A dispatch authorisation cannot use non-dispatch action classes.
[ ] A preflight trace cannot PASS with failed or blocking checks.
[ ] Temporal windows are semantically coherent.
[ ] Mission lifecycle state requires the corresponding stage references.
[ ] Commands are bound to payload, recipient, dispatch authorisation, expiry, and nonce.
[ ] Dispatch requires fresh current state where material.
[ ] Dispatch requires CP11 trace where CP11 is applicable.
[ ] Dispatch requires geofence/no-go relation validation.
[ ] Dispatch requires emergency stop, human override, and local fallback readiness where risk class/autonomy level demands it.
[ ] Dispatch requires compatible physical actor capability.
[ ] Agent-prepared candidates require agent trace and authority envelope.
[ ] Telemetry and receipts remain evidence candidates only.
[ ] Verification and accepted consequences remain separate.
[ ] Incidents and near misses do not auto-create compliance facts.
[ ] Conformance includes executable positive and negative fixtures.
```

---

# 7. Final hostile-review recommendation

```text
Acceptance recommendation: ACCEPT WITH CHANGES.
Do not return to Phase 0.
Do not split CP12.
Do not merge CP12.
Do not promote CP12 schemas to current/default.
Proceed to CP12 Phase 6.1 remediation.
```

CP12 is conceptually right and bounded. The RFC and baseline patch direction are sound. The machine-contract layer needs a strict hardening pass before final package assembly.

## Recommended next command

```text
Start CP12 Phase 6.1.

Using the CP12 Phase 6 hostile review, produce a CP12 remediation plan.

For each P0 and P1 defect, provide:
- exact RFC text change;
- exact baseline patch change if needed;
- exact schema change;
- exact conformance fixture change;
- whether the change is blocking for Phase 7.

Then produce revised schema-style definitions only for affected schemas, including at minimum:
- MissionDispatchAuthorization
- MissionPreflightTrace
- ExecutionWindow
- CommandEnvelope
- CommandIntegrityBasis
- CyberPhysicalMissionEnvelope
- EmergencyStopPolicy or EmergencyStopReadiness
- HumanOverridePolicy
- AutonomyLevelDeclaration
- PhysicalActorCapabilityProfile
- MissionCapabilityCompatibilityResult
- MissionScope or MissionPlan where CP11 applicability is modelled
- MissionOutputQualification
- MissionVerification
- MissionCandidate
- MissionSafetyConstraint
- MissionGeometryValidationResult if added

Do not create CP13, CP14, or CP15 contracts.
Do not claim robot/machine production readiness.
Keep all CP12 machine contracts in drafts_non_default.
```
