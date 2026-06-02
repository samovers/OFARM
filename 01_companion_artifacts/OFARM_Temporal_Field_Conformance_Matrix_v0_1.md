# OFARM Temporal Field Conformance Matrix v0.1

Date: 2026-05-14  
Status: active companion artifact; executable conformance guide  
Role: prevent timestamp collapse across observations, claims, execution, review, correction, materialization, and outputs

## Purpose

RC2.1 already distinguishes observation time, event time, assertion time, record time, effective time, review/decision time, supersession time, validity time, materialization time, and output time. This matrix makes that distinction easier to test.

## Core rule

A single timestamp must not be reused as every temporal fact in a high-consequence chain unless the record explicitly proves that the times are genuinely identical and policy accepts that identity. Delayed sync, manual correction, review, dispute, and materialization almost always require separate time semantics.

## Matrix

| Carrier | Required time semantics | Optional / contextual time semantics | Forbidden substitution |
|---|---|---|---|
| `AgronomicObservationContext` | `phenomenonTime` | linked `MeasurementEvidence.resultTime`, source/capture context | report/capture time must not replace observed phenomenon time |
| `MeasurementEvidence` | `resultTime` | `phenomenonTime`, sampling time, calibration time, custody timestamps | lab result time must not replace sampling/phenomenon time when distinct |
| `InterventionIntentPayload` | `createdAt`, `intendedTimeWindow` | authorization/review time, planned intervention time | created time must not prove execution time |
| `ExecutionRecordPayload` | `capturedAt`, `effectiveTimeInterval` | source payload capture time, review time, correction time, dispute time | captured time must not replace execution/effective interval |
| `AssertionRecord` | `assertedAt` | `occurrenceTime`, `effectiveFrom`, `effectiveUntil`, supersession/review refs | asserted time must not replace event occurrence time |
| `ReviewDecision` | decision time / reviewed-at field as defined by active schema | evidence receipt time, authority-evaluation time | review time must not rewrite original occurrence time |
| `AcceptedEventConsequence` | accepted/promoted consequence timing per schema | evidence, assertion, and review decision basis times | accepted time must not erase claim/evidence timing |
| `PartialExtent` | `createdAt`, `temporalApplicability` | geometry source/capture time, dispute/correction time | geometry creation time must not imply execution time |
| `CurrentStateMaterialization` | materialization time and basis/freshness time | invalidation time, basis-window time | materialization time must not become canonical event time |
| `PassportViewMetadata` | output generation time and source materialization/freshness basis | disclosure period, policy evaluation time | output time must not hide stale source state |
| `DocumentAssemblyMetadata` | assembly time and source artifact basis | annex/correction/dispute time | assembly time must not promote annexed material |

## Delayed-sync minimum

A delayed offline sync record must preserve, where applicable:

- when the work or observation occurred;
- when the source captured it;
- when the actor asserted or submitted it;
- when the platform received/synced it;
- when authority was evaluated;
- when review/correction/dispute occurred;
- when any current-state materialization or compiled output was generated.

## Conformance use

The semantic integrity runner checks positive and negative fixtures against this matrix. A collapsed-timestamp negative fixture should fail even when each individual date-time string is syntactically valid.
