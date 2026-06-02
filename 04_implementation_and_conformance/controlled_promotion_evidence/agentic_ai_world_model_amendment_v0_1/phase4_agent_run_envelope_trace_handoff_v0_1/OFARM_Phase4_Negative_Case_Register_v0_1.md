# OFARM Phase 4 Negative Case Register v0.1

Status: supporting review register; not promoted

| ID | Case | Expected result |
|---|---|---|
| P4-NC-001 | State-affecting run has no envelope | Deny or require envelope |
| P4-NC-002 | Envelope lacks actorship binding | Deny |
| P4-NC-003 | Tool outside allowed operations | Block and trace |
| P4-NC-004 | Write outside allowed surface | Block and trace |
| P4-NC-005 | Tool success used as governance success | Block promotion |
| P4-NC-006 | Handoff transfers authority by prompt | Deny; require receiving-agent authority |
| P4-NC-007 | Handoff exceeds SharingGrant | Redact or block |
| P4-NC-008 | Stale materialization used for high-consequence output | Recompute, downgrade, review, or block |
| P4-NC-009 | Permission-limited answer treated as absence | Block or require qualification |
| P4-NC-010 | Agent attempts pack activation | Block or route to human-governed path |
| P4-NC-011 | Revocation during long-running run | Retain trace; block final write |
| P4-NC-012 | Generic `AgentOutput` truth bucket used | Reject |
| P4-NC-013 | Conflict disappears during handoff | Block or preserve marker |
| P4-NC-014 | Agent scratch memory used as truth | Reject unless governed artifact |
| P4-NC-015 | Output preview treated as filed document | Block |
