# OFARM Authority Action Matrix — CP12 extension v0.1

Status: accepted/merged CP12 addendum; active below baseline authority. CP12 machine contracts remain draft/non-default.

## New CP12 action classes

| Action class | Default posture | Agent posture | Notes |
|---|---|---|---|
| MISSION_PREPARE_CANDIDATE | governed | allowed only within agent authority envelope | Candidate is not dispatch authority. |
| MISSION_REQUEST_PREFLIGHT | governed | allowed where explicit | Preflight has no side effects and grants no dispatch authority. |
| MISSION_APPROVE_DISPATCH | human or explicit bounded policy approval | not agent-default | Dispatch approval is high-consequence. |
| MISSION_DISPATCH_COMMAND | human or explicit bounded policy approval | not agent-default | Requires MissionDispatchAuthorization and CommandEnvelope. |
| MISSION_ABORT | allowed for authorised safety actors and local safety paths | allowed only where explicit emergency policy permits | Abort is safety-critical. |
| MISSION_EMERGENCY_STOP | always available through safety path | agent-default not required | Emergency stop must not depend on cloud/agent availability alone. |
| MISSION_OVERRIDE_TAKEOVER | authorised human/safety actor | not agent-default | Remote takeover is governed. |
| MISSION_REPORT_TELEMETRY | machine-reported with trace | allowed as evidence accepted/merged | Telemetry is not truth by itself. |
| MISSION_REPORT_EXECUTION_RECEIPT | machine/human reported with trace | allowed as evidence accepted/merged | Receipt is not verification. |
| MISSION_VERIFY_RESULT | authorised reviewer / verification pipeline | not agent-default for high consequence | Verification can support accepted consequence only through promotion law. |
| MISSION_ACCEPT_VERIFICATION | human or explicit bounded policy approval | not agent-default | High consequence. |
| MISSION_RECORD_NEAR_MISS | human/machine/agent report allowed | reporting only | Record does not auto-create compliance fact. |
| MISSION_RECORD_PHYSICAL_SAFETY_INCIDENT | human/machine report allowed | reporting only | High severity requires review. |
| MISSION_RESOLVE_PHYSICAL_SAFETY_INCIDENT | human/reviewer | not agent-default | Requires review/authority trace. |

Default rule: if the authority path is not explicit, deny.
