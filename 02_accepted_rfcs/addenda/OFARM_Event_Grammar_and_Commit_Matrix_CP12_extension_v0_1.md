# OFARM Event Grammar and Commit Matrix — CP12 extension v0.1

Status: accepted/merged CP12 addendum; active below baseline authority. CP12 machine contracts remain draft/non-default.

## CP12 event families

| Event | Commit posture | Consequence boundary |
|---|---|---|
| MissionIntentRecorded | planning/advisory | no dispatch authority |
| MissionCandidatePrepared | advisory/planning | no dispatch authority |
| MissionPlanApproved | governance/planning | not command |
| MissionPreflightCompleted | gate trace | not dispatch authority |
| MissionDispatchAuthorized | governance decision | dispatch authority only within scope/time/action |
| CommandEnvelopeCreated | command accepted/merged | not execution truth |
| CommandAcknowledged | evidence record | not proof of execution |
| MissionTelemetryReceived | evidence record | not accepted truth |
| MissionExecutionReceiptRecorded | evidence record | not verification |
| MissionVerificationRecorded | verification record | supports but does not bypass promotion |
| MissionAbortRecorded | event/evidence | not compliance fact by itself |
| EmergencyStopActivated | safety event | not compliance fact by itself |
| RemoteTakeoverRecorded | safety event | not compliance fact by itself |
| NearMissRecorded | safety event | high severity requires review |
| PhysicalSafetyIncidentRecorded | safety event | high severity requires review |

No CP12 event creates accepted execution consequence merely by existing.
