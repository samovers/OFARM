# CP12 Phase 6.1 — Remediation Plan

Status: remediation pass after CP12 Phase 6 hostile review.  
Package posture: draft/non-default machine contracts only.  
No CP13, CP14, or CP15 contracts are created.  
No robot/machine production readiness is claimed.

## 1. Remediation summary

| Defect | Severity | RFC text change | Baseline patch change | Schema change | Conformance fixture change | Blocking for Phase 7 |
|---|---:|---|---|---|---|---:|
| MissionDispatchAuthorization action class too broad | P0 | State that dispatch authorisation may only approve dispatch or dispatch command. | Add mission-authority action-class note. | Restrict `authorisedActionClass` to `MISSION_APPROVE_DISPATCH` and `MISSION_DISPATCH_COMMAND`. | Add bad telemetry/incident action fixtures and valid dispatch fixture. | Yes |
| Preflight can pass despite blocking failed checks | P0 | State that PASS requires all blocking checks to pass. | Add runtime preflight consistency rule. | Typed `checkResults`; semantic runner rejects PASS with blocking fail/review/insufficient. | Add preflight fail/pass fixtures. | Yes |
| Temporal coherence not enforced | P0 | Add temporal coherence rule for execution windows, commands, integrity, acknowledgements, dispatch. | Add runtime temporal coherence gate. | Add temporal fields and semantic checks. | Add inverted-window and valid-chain fixtures. | Yes |
| Mission lifecycle not tied to stage references | P0 | State that lifecycle claims require corresponding stage refs. | Add envelope lifecycle-stage consistency rule. | Conditional reference requirements in `CyberPhysicalMissionEnvelope`. | Add dispatched/verified/completed negative and positive fixtures. | Yes |
| Command payload integrity under-specified | P0 | Require digest and coverage of payload, mission, dispatch, recipient, expiry, nonce. | Add command-integrity gate. | `CommandIntegrityBasis` requires `commandPayloadDigestRef` and `signatureCovers` all binding elements. | Add missing digest/coverage fixtures. | Yes |
| Emergency-stop freshness/test gating missing | P0 | Dispatch-bound missions require fresh tested emergency-stop readiness. | Add mission safety readiness rule. | `EmergencyStopPolicy` requires test evidence, last-tested timestamp, freshness state. | Add untested/stale/fresh fixtures. | Yes |
| Human override/supervision under-enforced | P0 | M3/M4/high-risk require override/supervision/fallback. | Add autonomy/supervision rule. | `HumanOverridePolicy` and `AutonomyLevelDeclaration` hardened. | Add M3/M4 invalid/valid fixtures. | Yes |
| Physical capability compatibility too weak | P0 | Dispatch requires fresh compatibility check. | Add capability compatibility gate. | `MissionDispatchAuthorization` requires compatibility result refs; compatibility schema requires fresh verified capability for COMPATIBLE. | Add no-compatibility/stale/valid fixtures. | Yes |
| CP11 applicability under-modelled | P0 | Mission dispatch must resolve CP11 applicability. | Add CP11 applicability gate to CP12. | `cp11ApplicabilityState` added to scope/plan/dispatch. | Add applicable-without-trace and valid trace fixtures. | Yes |
| Geofence/no-go relation not executable | P0 | Add geometry validation result as dispatch precondition. | Add geometry-relation rule. | New `MissionGeometryValidationResult`; scope requires geometry validation result refs. | Add no-go overlap/CRS/stale/valid fixtures. | Yes |
| MissionOutputQualification too permissive | P0/P1 | Advisory mission outputs cannot be filed/claims/dispatch/execution truth. | Add output disposition consistency rule. | Conditional blocked-use requirements; no-overlap semantic check. | Add advisory filed/claim bad and valid report fixtures. | Yes |
| Conformance plan not executable | P0 | RFC must require executable fixtures, not names only. | Readiness claim remains blocked until runner passes. | Schema-aware and semantic-hardening-aware runner included. | Positive and negative fixture set included. | Yes |
| MissionVerification inconsistent | P1 | Failed verification cannot carry accepted consequence candidates. | None beyond output/consequence boundary. | Conditional verification-disposition rules. | Add failed/verified fixtures. | Yes before Phase 7 schemas final |
| Agent-prepared candidate trace weak | P1 | Agent-prepared candidates require agent run trace and authority envelope. | None; uses existing agent law. | Add `preparedByActorClass` and conditional requirements. | Add agent candidate fixtures. | Yes before Phase 7 schemas final |
| Command acknowledgement not validity linked | P1 | Late acknowledgement must be rejected/expired. | None beyond temporal gate. | Add command validity snapshot fields; runner enforces. | Add late ack fixtures. | Yes before Phase 7 schemas final |
| Safety constraints allow advisory critical requirements | P1 | Critical safety requirements are not advisory warnings for dispatch. | Add safety-constraint posture note. | Conditional rule prevents advisory warning for emergency stop, override, fallback, command integrity, geofence, no-go. | Add advisory-critical safety negative fixtures. | Yes before Phase 7 schemas final |
| Mission pack support only hook | P1 | Keep mission pack support draft/non-default until pack currentness update. | Readiness/non-claims note. | No new active pack contracts in this remediation. | Fixture list records future pack-hardening cases only. | No, if labelled |

## 2. Revised affected schemas

This package provides remediated draft/non-default schema-style definitions for affected CP12 contracts only. The schemas are staged under:

```text
03_machine_contracts/drafts_non_default/cyber_physical_mission/
```

They use:

```text
schemaVersion: cp12-v0.1-draft-phase6-1-remediated
```

## 3. Minimum P0 runner specification

The conformance runner must be:

- JSON-Schema-aware;
- semantic-hardening-aware for temporal and cross-field constraints that JSON Schema cannot express safely;
- fixture-driven with explicit expected pass/fail;
- able to reject syntactically valid but semantically unsafe records.

Semantic checks implemented in this package include:

- preflight PASS cannot coexist with blocking failed/review/insufficient checks;
- temporal windows must be coherent;
- command envelopes must be inside resolved execution-window and dispatch-validity bounds when supplied;
- command integrity expiry must be after command creation;
- command acknowledgement after expiry cannot be RECEIVED/ACCEPTED;
- mission output allowed/blocked classes must be disjoint;
- safety-critical MissionSafetyConstraint classes cannot be advisory-only;
- geometry validation cannot PASS with no-go overlap, CRS mismatch, stale geometry, or failed containment;
- MissionOutputQualification cannot treat advisory-only output as filed/claim/attestation/dispatch/execution truth;
- capability compatibility cannot be compatible with stale or unverified capability;
- MissionVerification cannot produce accepted-consequence candidates from failed/disputed verification.

## 4. Phase 7 blocking status

Proceed to CP12 Phase 7 only if:

- schemas validate;
- positive and negative fixtures pass;
- draft/non-default currentness is preserved;
- no CP13, CP14, or CP15 law is introduced;
- no robot/machine production readiness is claimed.
