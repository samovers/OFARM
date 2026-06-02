# OFARM Phase 3 Negative Case Register v0.1

Date: 2026-05-14  
Status: supporting review note

The following cases must be blocked or routed to review/human approval by any future implementation claiming Phase 3 conformance.

| Case | Expected outcome |
|---|---|
| Missing agent sponsor | DENY |
| Accountable party ambiguous | DENY or REQUIRE_REVIEW |
| Unknown agent instance | DENY |
| Suspended or revoked agent instance | DENY |
| Model/tool profile unapproved for requested use | DENY or downgrade to SUGGEST/DRAFT only |
| Agent requests human-governed action class | DENY or REQUIRE_HUMAN_APPROVAL |
| Agent acts outside grant scope | DENY |
| Agent acts after grant/delegation expiry | DENY |
| Revocation occurs during prepared flow | Final action DENY or REQUIRE_REVIEW |
| Prompt text says “human approved” but no approval record exists | DENY |
| Tool call succeeds but authority failed | DENY; no governed artifact promotion |
| Agent-generated recommendation tries to become compliance fact | DENY |
| Agent creates generic `AgentOutput` truth bucket | DENY |
| Agent uses model memory as source truth | DENY unless persisted as governed artifact and promoted normally |
| Agent treats permission-limited answer as absence of records | DENY or result qualification required |
