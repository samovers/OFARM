# OFARM Phase 3 Agent Authority Trace Requirements v0.1

Date: 2026-05-14  
Status: supporting review note

An `AgentAuthorizationDecisionTrace` should explain at minimum:

1. requested action class;
2. target twin, target scope, and target time;
3. accountable party and sponsor role;
4. agent profile and instance lifecycle state;
5. model/tool profile approval state;
6. authority grant, delegation envelope, or sharing grant basis;
7. scope inheritance mode applied;
8. revocation checks performed;
9. human-approval or review requirement;
10. output disposition allowed or denied;
11. decision outcome;
12. reason codes;
13. trace-back refs to policy/evidence/runtime records.

The trace does not need to expose proprietary neural-model internals. It must expose enough governed basis to explain why OFARM allowed, denied, required review, or required human approval.
