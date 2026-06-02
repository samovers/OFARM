# OFARM Phase 5 Negative Case Register

| Case | Description | Expected result |
|---|---|---|
| P5-NC-001 | Tool declares `readOnlyHint=true` but its effect class is state-affecting | Blocked or human-governed preflight required |
| P5-NC-002 | Capability Manifest declares `agentSupport.supported=true`, but no AgentToolManifest is referenced | Manifest invalid or incomplete |
| P5-NC-003 | AgentToolManifest lists a tool with no required authority basis | Manifest invalid |
| P5-NC-004 | Tool descriptor says human approval is not required for pack activation | Manifest invalid or tool not agent-callable |
| P5-NC-005 | Manifest declares runtime readiness with no runtime evidence | Readiness claim rejected |
| P5-NC-006 | World-model support declares Compliance Twin mutation | Manifest invalid |
| P5-NC-007 | Tool prepares external disclosure without SharingGrant or redaction policy | Blocked |
| P5-NC-008 | Farm-data learning policy defaults to cross-farm learning | Invalid unless explicit opt-in grant is present |
| P5-NC-009 | Tool output disposition is generic `AgentOutput` | Invalid |
| P5-NC-010 | Manifest claims two-agent compatibility without executed conformance | Claim rejected |
